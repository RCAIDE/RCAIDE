# RCAIDE/Library/Methods/Mass/Correlation/Transport/horizontal_tail.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created:  May 2024, J. Smart
# Modified:

# ----------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------- 

from RCAIDE.Reference.Core import Units

import numpy as np

# -----------------------------------------------------------------------
# Functional/Library Version
# -----------------------------------------------------------------------

def func_horizontal_tail(wingspan : float,
                         quarter_chord_sweep : float,
                         thickness_to_chord : float,
                         reference_area : float,
                         exposed_area : float,
                         wetted_area : float,
                         vehicle_max_takeoff_weight : float,
                         vehicle_ultimate_load : float,
                         main_wing_mean_aerodynamic_chord : float,
                         moment_arm_length : float,
                         ):
    """ Calculate the weight of the horizontal tail in a standard configuration

            Assumptions:
                calculated weight of the horizontal tail including the elevator
                Assume that the elevator is 25% of the horizontal tail

            Source:
                Aircraft Design: A Conceptual Approach by Raymer

            Inputs:
                wing.spans.projected - span of the horizontal tail                                              [meters]
                wing.sweeps.quarter_chord - sweep of the horizontal tail                                        [radians]
                Nult - ultimate design load of the aircraft                                                     [dimensionless]
                S_h - area of the horizontal tail                                                               [meters**2]
                vehicle.mass_properties.max_takeoff - maximum takeoff weight of the aircraft                    [kilograms]
                vehicle.wings['main_wing'].origin[0] - mean aerodynamic chord of the wing                       [meters]
                wing.aerodynamic_center[0]  - mean aerodynamic chord of the horizontal tail                     [meters]
                wing.thickness_to_chord  - thickness-to-chord ratio of the horizontal tail                      [dimensionless]
                wing.areas.exposed - exposed surface area for the horizontal tail                               [m^2]
                wing.areas.wetted - wetted surface area of tail

            Outputs:
                weight - weight of the horizontal tail                                                          [kilograms]

            Properties Used:
                N/A
            """

    # Unit Conversion

    b = wingspan / Units.ft
    S = reference_area / Units.ft ** 2
    MTOW = vehicle_max_takeoff_weight / Units.lbm
    MAC = main_wing_mean_aerodynamic_chord / Units.ft
    L = moment_arm_length / Units.ft

    # Shorthand Aliases
    exr = np.sqrt(exposed_area * S/ wetted_area)
    tc = thickness_to_chord
    qc = quarter_chord_sweep

    mass = (5.25 * S +
            8E-7 * vehicle_ultimate_load * b ** 3 * MTOW * MAC * exr /
            (tc * np.cos(qc)**2 * L * S**1.5)) * Units.lbs


    return mass


# -----------------------------------------------------------------------
# Stateful/Framework Version
# -----------------------------------------------------------------------

def horizontal_tail(State, Settings, System):


    h_tail = System.wings.horizontal_tail

    wingspan                            = h_tail.spans.projected
    quarter_chord_sweep                 = h_tail.sweeps.quarter_chord
    thickness_to_chord                  = h_tail.thickness_to_chord
    reference_area                      = h_tail.areas.reference
    exposed_area                        = h_tail.areas.exposed
    wetted_area                         = h_tail.areas.wetted

    vehicle_max_takeoff_weight          = System.mass_properties.max_takeoff
    vehicle_ultimate_load               = System.envelope.ultimate_load

    main_wing = System.wings.main_wing


    main_wing_mean_aerodynamic_chord    = main_wing.chords.mean_aerodynamic
    moment_arm_length                   = (h_tail.origin[0] + h_tail.aerodynamic_center[0] -
                                          (main_wing.origin[0] + main_wing.aerodynamic_center[0]))

    h_tail_mass = func_horizontal_tail(wingspan,
                                   quarter_chord_sweep,
                                   thickness_to_chord,
                                   reference_area,
                                   exposed_area,
                                   wetted_area,
                                   vehicle_max_takeoff_weight,
                                   vehicle_ultimate_load,
                                   main_wing_mean_aerodynamic_chord,
                                   moment_arm_length)

    h_tail.mass_properties.total = h_tail_mass * (1. - Settings.mass_reduction_factors.empennage)

    System.sum_mass()

    return State, Settings, System
