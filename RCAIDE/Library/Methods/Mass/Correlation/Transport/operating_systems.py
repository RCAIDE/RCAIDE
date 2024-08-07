# RCAIDE/Library/Methods/Mass/Correlation/Transport/operating_systems.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created:  May 2024, J. Smart
# Modified:

# ----------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------- 

import numpy as np
from RCAIDE.Reference.Core import Units
from RCAIDE.Framework.Components import Component
from RCAIDE.Framework.Components.Wings import Horizontal_Tail, Vertical_Tail, Main_Wing

# -----------------------------------------------------------------------
# Functional/Library Version
# -----------------------------------------------------------------------

def func_operating_systems(fixed_masses : np.ndarray,
                           per_seat_masses : np.ndarray,
                           number_of_seats : int,
                           reference_area : float,
                           tail_area : float,
                           full_powered_controls : bool = True,
                           partially_powered_controls : bool = False,
                           *args, **kwargs):

    # Total Operating System Mass
    total_opsys_mass = (np.sum(fixed_masses)
                        + np.sum(per_seat_masses) * number_of_seats)

    # Flight Control System Mass

    fc_scaler = (1.7                                # 1.7 if Fully Aerodynamic
                 + 0.8 * partially_powered_controls # 2.5 if Partially Powered
                 + 1.8 * full_powered_controls)     # 3.5 if Fully Powered

    tail_area_imp = tail_area / Units.ft ** 2

    fc_mass = (fc_scaler * tail_area_imp) * Units.lbm

    # Hydraulics & Pneumatics System Mass

    hp_mass = (0.65 * reference_area) * Units.lbm

    return total_opsys_mass, fc_mass, hp_mass


# -----------------------------------------------------------------------
# Stateful/Framework Version
# -----------------------------------------------------------------------

def operating_systems(State, Settings, System):

    fixed_masses = []
    fixed_mass_names = []

    per_seat_masses = []
    per_seat_mass_names = []

    adjustment = 1.0 - Settings.mass_reduction_factors.systems

    for key, value in System.aircraft_type.__dict__.items():
        if key[-4:] == 'mass' and value.metadata['fixed']:
            fixed_masses.append(value)
            fixed_mass_names.append(key)
        elif key[-4:] =='mass' and value.metadata['per_seat']:
            per_seat_masses.append(value)
            per_seat_mass_names.append(key)

    s_tail = 0.
    for wing in System.wings:
        if isinstance(wing, Horizontal_Tail) or isinstance(wing, Vertical_Tail):
            s_tail += wing.areas.reference

    if s_tail == 0:
        for wing in System.wings:
            if isinstance(wing, Main_Wing):
                s_tail += wing.areas.reference * 0.01

    results = func_operating_systems(np.asarray(fixed_masses),
                                     np.asarray(per_seat_masses),
                                     System.number_of_passengers,
                                     System.reference_area,
                                     s_tail)

    total_opsys_mass    = results[0] * adjustment
    fc_mass             = results[1] * adjustment
    hp_mass             = results[2] * adjustment

    if not hasattr(System, 'operating_systems'):
        System.add_subcomponent(Component(name='operating_systems'))

    output = System.operating_systems.mass_properties
    output.total = total_opsys_mass

    if not hasattr(output, 'flight_controls'):
        output.add_subcomponent(Component(name='flight_controls'))

    output.flight_controls.mass_properties.total = fc_mass

    if not hasattr(output, 'hydraulics'):
        output.add_subcomponent(Component(name='hydraulics'))

    output.hydraulics.mass_properties.total = hp_mass

    for i in range(len(fixed_mass_names)):
        if not hasattr(output, fixed_mass_names[i]):
            output.add_subcomponent(Component(name=fixed_mass_names[i]))
        output.__dict__[fixed_mass_names[i]].mass_properties.total = (
            fixed_masses[i] * adjustment)

    for i in range(len(per_seat_mass_names)):
        if not hasattr(output, per_seat_mass_names[i]):
            output.add_subcomponent(Component(name=per_seat_mass_names[i]))
        output.__dict__[per_seat_mass_names[i]].mass_properties.total = (
                per_seat_masses[i] * System.number_of_passengers * adjustment)

    output.sum_mass()
    System.sum_mass()

    return State, Settings, System
