# RCAIDE/Library/Methods/Mass/Correlation/Transport/operating_systems.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created:  May 2024, J. Smart
# Modified:

# ----------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------- 

# package imports
import jax
import jax.numpy as jnp
from RCAIDE.Library import Units

import RCAIDE.Framework as rcf
import RCAIDE.Library as rcl

# -----------------------------------------------------------------------
# Functional/Library Version
# -----------------------------------------------------------------------

def func_operating_systems(fixed_masses : jnp.ndarray,
                           per_seat_masses : jnp.ndarray,
                           number_of_seats : int,
                           reference_area : float,
                           tail_area : float,
                           full_powered_controls : bool = True,
                           partially_powered_controls : bool = False,
                           *args, **kwargs):

    # Total Operating System Mass
    total_opsys_mass = (jnp.sum(fixed_masses)
                        + jnp.sum(per_seat_masses) * number_of_seats)

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

def operating_systems(state: "rcf.State",
                      system: "rcf.Aircraft",
                      settings: "rcf.Settings",):

    fixed_masses = []
    fixed_mass_names = []

    per_seat_masses = []
    per_seat_mass_names = []

    adjustment = 1.0 - settings.mass_reduction_factors.systems

    fixed_array     = jnp.array(jax.tree_util.tree_leaves(system.ac_class.fixed_masses))
    per_seat_array  = jnp.array(jax.tree_util.tree_leaves(system.ac_class.per_seat_masses))

    s_tail = 0.
    for wing in system.wings:
        if isinstance(wing, Horizontal_Tail) or isinstance(wing, Vertical_Tail):
            s_tail += wing.areas.reference

    if s_tail == 0:
        for wing in system.wings:
            if isinstance(wing, Main_Wing):
                s_tail += wing.areas.reference * 0.01

    results = func_operating_systems(fixed_array,
                                     per_seat_array,
                                     system.number_of_passengers,
                                     system.reference_area,
                                     s_tail)

    total_opsys_mass    = results[0] * adjustment
    fc_mass             = results[1] * adjustment
    hp_mass             = results[2] * adjustment

    if not hasattr(system, 'operating_systems'):
        system.add_subcomponent(rcl.Component(tag='operating_systems'))

    output = system.operating_systems.mass_properties
    output.total = total_opsys_mass

    if not hasattr(output, 'flight_controls'):
        output.add_subcomponent(rcl.Component(tag='flight_controls'))

    output.flight_controls.mass_properties.total = fc_mass

    if not hasattr(output, 'hydraulics'):
        output.add_subcomponent(rcl.Component(tag='hydraulics'))

    output.hydraulics.mass_properties.total = hp_mass

    for i in range(len(fixed_mass_names)):
        if not hasattr(output, fixed_mass_names[i]):
            output.add_subcomponent(rcl.Component(tag=fixed_mass_names[i]))
        output.__dict__[fixed_mass_names[i]].mass_properties.total = (
            fixed_masses[i] * adjustment)

    for i in range(len(per_seat_mass_names)):
        if not hasattr(output, per_seat_mass_names[i]):
            output.add_subcomponent(rcl.Component(tag=per_seat_mass_names[i]))
        output.__dict__[per_seat_mass_names[i]].mass_properties.total = (
                per_seat_masses[i] * system.number_of_passengers * adjustment)

    output.sum_mass()
    system.sum_mass()

    return state, system, settings
