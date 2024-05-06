# RCAIDE/Library/Methods/Mass/Correlation/Transport/vertical_tail.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created:  May 2024, J. Smart
# Modified:

# ----------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------- 

# TODO: ADD IMPORTS

# -----------------------------------------------------------------------
# Functional/Library Version
# -----------------------------------------------------------------------

def func_vertical_tail(wingspan : float,
                       quarter_chord_sweep : float,
                       thickness_to_chord : float,
                       reference_area : float,
                       rudder_fraction : float,
                       vehicle_maximum_takeoff_weight : float,
                       vehicle_reference_area : float,
                       vehicle_ultimate_load : float
                       ):
    """ Calculate the weight of the vertical fin of an aircraft without the weight of
        the rudder and then calculate the weight of the rudder

        Assumptions:
            Vertical tail weight is the weight of the vertical fin without the rudder weight.
            Rudder occupies 25% of the S_v and weighs 60% more per unit area.

        Source:
            N/A

        Inputs:
            S_v - area of the vertical tail (combined fin and rudder)                      [meters**2]
            vehicle.envelope.ultimate_load - ultimate load of the aircraft                 [dimensionless]
            wing.spans.projected - span of the vertical                                    [meters]
            vehicle.mass_properties.max_takeoff - maximum takeoff weight of the aircraft   [kilograms]
            wing.thickness_to_chord- thickness-to-chord ratio of the vertical tail         [dimensionless]
            wing.sweeps.quarter_chord - sweep angle of the vertical tail                   [radians]
            vehicle.reference_area - wing gross area                                       [meters**2]
            wing.t_tail - factor to determine if aircraft has a t-tail                     [dimensionless]
            rudder_fraction - fraction of the vertical tail that is the rudder             [dimensionless]

        Outputs:
            output - a dictionary with outputs:
                wt_tail_vertical - weight of the vertical fin portion of the vertical tail [kilograms]
                wt_rudder - weight of the rudder on the aircraft                           [kilograms]

        Properties Used:
            N/A
        """

    b = wingspan / Units.ft
    S = reference_area / Units.ft ** 2
    MTOW = vehicle_maximum_takeoff_weight / Units.lbm
    Sref = vehicle_reference_area / Units.ft ** 2

    # Shorthand Aliases
    tc = thickness_to_chord
    qc = quarter_chord_sweep

    v_tail_mass = (2.62 * S * 1.5E-5 *
                   vehicle_ultimate_load * b**3 *
                   (8. + 0.44 * MTOW / Sref) /
                   (tc * np.cos(qc)**2)) * Units.lbs

    v_tail_mass += rudder_fraction * 1.6

    return v_tail_mass


# -----------------------------------------------------------------------
# Stateful/Framework Version
# -----------------------------------------------------------------------

def vertical_tail(State, Settings, System):

    v_tail = System.wings.vertical_tail

    wingspan                        = v_tail.spans.projected
    quarter_chord_sweep             = v_tail.sweeps.quarter_chord
    thickness_to_chord              = v_tail.thickness_to_chord
    reference_area                  = v_tail.areas.reference

    rudder_fraction                 = Settings.sizing.rudder_fraction

    vehicle_maximum_takeoff_weight  = System.mass_properties.max_takeoff
    vehicle_reference_area          = System.areas.reference
    vehicle_ultimate_load           = System.envelope.ultimate_load

    v_tail_mass = func_vertical_tail(wingspan,
                                     quarter_chord_sweep,
                                     thickness_to_chord,
                                     reference_area,
                                     rudder_fraction,
                                     vehicle_maximum_takeoff_weight,
                                     vehicle_reference_area,
                                     vehicle_ultimate_load
                                     )


    v_tail.mass_properties.mass = v_tail_mass * (1. - Settings.mass_reduction_factors.empennage)

    System.sum_mass()

    return State, Settings, System
