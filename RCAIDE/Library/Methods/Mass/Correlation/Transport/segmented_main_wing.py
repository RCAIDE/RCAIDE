# RCAIDE/Library/Methods/Mass/Correlation/Transport/segmented_main_wing.py
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

def func_segmented_main_wing(wingspan: float,
                             wing_reference_area: float,
                             wing_root_chord : float,
                             segment_quarter_chord_sweeps: list[float],
                             segment_percent_span_locations: list[float],
                             segment_thickness_to_chord: list[float],
                             segment_root_chord_percents: list[float],
                             material_density: float,
                             material_yield_tensile_strength: float,
                             vehicle_reference_area: float,
                             vehicle_ultimate_load_factor: float,
                             vehicle_maximum_takeoff_weight: float,
                             vehicle_zero_fuel_weight: float):

    #---------------------------------------------------------------------------
    # Preliminary Calculations
    #---------------------------------------------------------------------------

    area_fraction   = wing_reference_area / vehicle_reference_area

    strength_ratio  = (material_density * 9.81 * Units['m/(s**2)'] /
                       material_yield_tensile_strength)

    mass_geometric_mean = np.sqrt(vehicle_maximum_takeoff_weight *
                                  vehicle_zero_fuel_weight) / Units['kg']

    maximum_load = (vehicle_ultimate_load_factor *
                    mass_geometric_mean * 9.81 * Units['m/(s**2)']) / Units['N']

    root_aerodynamic_load = (area_fraction * 2 * maximum_load /
                            (wingspan * np.pi))

    #---------------------------------------------------------------------------
    # Similar/Dissimilar Segments
    #---------------------------------------------------------------------------

    # Find segment transitions without big jumps in root chord percents or
    # thickness to chord ratios

    small_jumps = ( np.isclose(np.diff(segment_root_chord_percents), 0.)
                  * np.isclose(np.diff(segment_thickness_to_chord), 0.))

    # +1 offset to get segments following small jumps
    similar_segments = np.where(small_jumps)[0] + 1

    # Logical -1 to get segments without small jumps
    dissimilar_segments = np.where(1-small_jumps)[0] + 1

    #---------------------------------------------------------------------------
    # Similar Segment Sum
    #---------------------------------------------------------------------------

    def span_factor(x: np.ndarray) -> np.ndarray:
        return 1/8 * (x * (5 - 2 * x**2) * np.sqrt(1 - x**2) + 3 * np.arcsin(x))

    # Root Chord
    rc = np.array([segment_root_chord_percents[i]
                  for i in similar_segments])[1:] * wing_root_chord

    # Thickness to Chord
    tc = np.array([segment_thickness_to_chord[i]
                  for i in similar_segments])[1:]

    # Previous Segments Quarter Chord Sweeps
    sw = np.array([segment_quarter_chord_sweeps[i]
                  for i in similar_segments])[:-1]

    # Percent Span Locations
    sp = np.array([segment_percent_span_locations[i]
                  for i in similar_segments])[1:]

    # Previous Segments Percent Span Locations
    sr = np.array([segment_percent_span_locations
                  for i in similar_segments])[:-1]

    similar_segment_sum = np.sum(
        np.real(
            (1 / (tc * rc * np.cos(sw ** 2))
             * 1 / 3 * (
                     span_factor(sp)
                     - span_factor(sr)
             )  # Close Span Factors Calculation
             )  # Close Sweep Factor Calculation
        )  # Close Real Part Calculation
    )  # Close Summation Calculation

    #---------------------------------------------------------------------------
    # Dissimilar Segment Sum
    #---------------------------------------------------------------------------

    # Root Chord
    drc = np.array([segment_root_chord_percents[i]
                   for i in dissimilar_segments])[1:] * wing_root_chord

    # Previous Segments Root Chord
    drr = np.array([segment_root_chord_percents[i]
                    for i in dissimilar_segments])[:-1] * wing_root_chord

    # Thickness to Chord
    dtc = np.array([segment_thickness_to_chord[i]
                   for i in dissimilar_segments])[1:]

    # Previous Segments Thickness to Chord
    dtr = np.array([segment_thickness_to_chord[i]
                   for i in dissimilar_segments])[:-1]

    # Previous Segments Quarter Chord Sweeps
    dsw = np.array([segment_quarter_chord_sweeps[i]
                   for i in dissimilar_segments])[:-1]

    # Percent Span Locations
    dsp = np.array([segment_percent_span_locations[i]
                   for i in dissimilar_segments])[1:]

    # Previous Segments Percent Span Locations
    dsr = np.array([segment_percent_span_locations[i]
                   for i in dissimilar_segments])[:-1]

    # Derived Statistics

    drt = drr * dtr  # Root Thicknesses
    dts = (drt - drc * dtc) / (dsp - dsr)  # Thickness slopes
    def span_integral(x: A=drt, B=dts, C=dsr) -> np.ndarray:
        """ Integrate the wing bending moment over a section

            Assumptions:
                Linearly tapering thickness

            Source:
                Botero 2019

            Inputs:
                x - span wise station      [dimensionless]
                A - origin thickness       [meters]
                B - taper ratio of section [dimensionless]
                C - origin offset          [dimensionless]

            Outputs:
                result - evaluate one side of an indefinite integral [meters^-1]

            Properties Used:
                N/A
            """

        # Shorthand Aliases/Redundant Calculations
        xsq = x ** 2
        xsqC = np.sqrt(1 - xsq)
        xas = np.arcsin(x)

        Asq = A ** 2
        Acb = A ** 3

        Bsq = B ** 2
        Bcb = B ** 3

        Csq   = C ** 2
        CsqC  = -1 + Csq
        Csq2C = -1 + 2 * Csq
        Csq3C = -1 + 3 * Csq

        ABC = A * B * C
        ApBC = A + B * C

        Q   = np.sqrt(0j - Asq -2*ABC - Bsq*CsqC)
        Qsq = np.sqrt(0j - (Asq + 2 * ABC + Bsq * CsqC) ** 2)
        QB  = np.sqrt(0j - Asq + Bsq - 2 * ABC - Bsq * Csq)
        Q2  = 2*Asq + 4*ABC + Bsq*Csq2C
        Q3  = 4 * (Acb + 3 * A*ABC + Bcb * C * CsqC + A * Bsq * Csq3C) * x

        V   = np.log(A + B * C - B * x)
        V2  = np.log(0j - ApBC + B * x)
        V3  = np.log(0j - B + ApBC * x - Q * xsqC)
        V4  = np.log(-B + ApBC*x + QB * xsqC)
        V5  = np.log(x * (Asq + 2 * ABC + Bsq * CsqC) + Qsq * xsqC)

        pi = np.pi

        res =   (
                (1 / (4*Bcb)) * (
                    pi*x *  (
                            2      *   Asq +
                            4      *   ABC  +
                            Bsq    *   Csq2C
                            ) -
                    xsqC *  (
                            2      *   Q2   +
                            2/3    *   B
                            ) *
                    (3 * A * x + B * (-1 + 3 * C * x + xsq)) +
                    xas *   (
                            2*B     *   ApBC-
                            2*Q2    *   x
                            ) -
                    (4*ApBC**2 * Q * V) / B -
                    (Q3 * V) / Q +
                    (8*ApBC**2 * Q * V2) / B +
                    (Q3 * V3) / Q -
                    4*ApBC/B*(
                            ApBC * Q * V4 +
                            Qsq * V5
                            )
                    )
                )

        return res

    dissimilar_segment_sum = np.sum(
        np.real(
            (span_integral(dsp) - span_integral(dsr)/
            np.cos(dsw ** 2))
        )
    )

    segment_sum = similar_segment_sum + dissimilar_segment_sum

    stress_mass = (strength_ratio *
                   wingspan**2 *
                   root_aerodynamic_load *
                   segment_sum /2) / Units.lbm

    mass = 4.22 * wing_reference_area/Units['ft**2'] + stress_mass

    return mass


# -----------------------------------------------------------------------
# Stateful/Framework Version
# -----------------------------------------------------------------------

def segmented_main_wing(State, Settings, System):

    wing = System.wings.main_wing

    wingspan                        = wing.spans.projected
    wing_reference_area             = wing.areas.reference
    wing_root_chord                 = wing.chords.root

    segments = wing.segments

    segment_quarter_chord_sweeps    = [s.quarter_chord_sweep for s in segments]
    segment_percent_span_locations  = [s.percent_span_location for s in segments]
    segment_thickness_to_chord      = [s.thickness_to_chord for s in segments]
    segment_root_chord_percents     = [s.root_chord_percent for s in segments]


    material = wing.material_properties.tensile_stress_carrier

    material_density                = material.density
    material_yield_tensile_strength = material.yield_tensile_strength

    vehicle_reference_area          = System.areas.reference
    vehicle_ultimate_load_factor    = System.envelope.ultimate_load
    vehicle_maximum_takeoff_weight  = System.mass_properties.max_takeoff
    vehicle_zero_fuel_weight        = System.mass_properties.max_zero_fuel

    main_wing_mass = func_segmented_main_wing(wingspan,
                                              wing_reference_area,
                                              wing_root_chord,
                                              segment_quarter_chord_sweeps,
                                              segment_percent_span_locations,
                                              segment_thickness_to_chord,
                                              segment_root_chord_percents,
                                              material_density,
                                              material_yield_tensile_strength,
                                              vehicle_reference_area,
                                              vehicle_ultimate_load_factor,
                                              vehicle_maximum_takeoff_weight,
                                              vehicle_zero_fuel_weight)

    wing.mass_properties.mass = main_wing_mass * (1. - Settings.mass_reduction_factors.main_wing)

    System.sum_mass()

    return State, Settings, System
