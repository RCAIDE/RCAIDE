# RCAIDE/Methods/Aerodynamics/Common/Drag/parasite_drag_wing.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
from RCAIDE.Framework.Core import Data  
from RCAIDE.Library.Methods.Geometry.Planform.wing_segmented_planform import segment_properties

# legacy imports 
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Helper_Functions import compressible_mixed_flat_plate
from Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.Cubic_Spline_Blender import Cubic_Spline_Blender
 
# package imports
import numpy as np  

# ----------------------------------------------------------------------------------------------------------------------  
#   Parasite Drag Wing 
# ----------------------------------------------------------------------------------------------------------------------
def parasite_drag_wing(state, settings, geometry):
    """Computes the parasite drag due to wings

    Assumptions: 

    Source:
        http://aerodesign.stanford.edu/aircraftdesigNoneircraftdesign.html (Stanford AA241 A/B Course Notes)

    Args:
        settings.wing_parasite_drag_form_factor             (float): wing parasite drag form factor              [unitless]
        state.conditions.freestream.mach_number     (numpy.ndarray): mach number                                 [unitless] 
        state.conditions.freestream.temperature     (numpy.ndarray): temperature                                 [K]
        state.conditions.freestream.reynolds_number (numpy.ndarray): reynolds number                             [unitless] 
        geometry.areas.reference                            (float): reference area                              [m^2]
        geometry.chords.mean_aerodynamic                    (float): mean aerodynamic chord                      [m]
        geometry.thickness_to_chord                         (float): thickness to chord ratio                    [unitless]
        geometry.sweeps.quarter_chord                       (float): quarter chord sweep                         [radians]
        geometry.aspect_ratio                               (float): aspect ratio                                [unitless]
        geometry.spans.projected                            (float): projected span                              [m]
        geometry.areas.affected                             (float): affected area                               [m^2]
        geometry.areas.wetted                               (float): wetted area                                 [m^2]
        geometry.transition_x_upper                         (float): transition point on upper surface of wing   [unitless]
        geometry.transition_x_lower                         (float): transition point on lower surface of wing   [unitless]
      
      
    Returns:
        state.conditions.aerodynamics.coefficients.drag
            .parasite[wing.tag].wetted_area                            (float): wetted_area               [m^2]
            .parasite[wing.tag].parasite_drag      (numpy.ndarray): parasite_drag [unitess]
            .parasite[wing.tag].skin_friction      (numpy.ndarray): skin_friction [unitess]
            .parasite[wing.tag].compressibility_factor                 (float): compressibility_factor    [unitess]
            .parasite[wing.tag].reynolds_factor                (numpy.ndarray): reynolds_factor           [unitess]
            .parasite[wing.tag].form_factor                            (float): form_factor               [unitess]
    """
    
    # Unpack inputs
    C                             = settings.wing_parasite_drag_form_factor
    recalculate_total_wetted_area = settings.recalculate_total_wetted_area
    freestream                    = state.conditions.freestream
    
    # Unpack conditions
    Mc  = freestream.mach_number
    Tc  = freestream.temperature    
    re  = freestream.reynolds_number

    # Unpack wing
    span_offset  = geometry.percent_span_root_offset
    t_c_w        = geometry.thickness_to_chord
    Sref         = geometry.areas.reference
    xtu          = geometry.transition_x_upper
    xtl          = geometry.transition_x_lower

    # Define a function to compute parasite drag for a single segment
    def _single_segmented(segment):

        # Unpack Geometry

        mac         = geometry.chords.mean_aerodynamic
        sweep       = geometry.sweeps.quarter_chord
        span        = geometry.spans.projected
        seg_Sref    = geometry.areas.reference
        seg_Swet    = geometery.areas.wetted
        chord_root  = geometry.chords.root
        chord_tip   = geometry.chords.tip

        # Derived Quantities

        wing_root = chord_root + span_offset * ((chord_tip - chord_root) / span)
        re_w = re * mac

        # Optionally recalculate total wetted area if not provided

        if recalculate_total_wetted_area or seg_Swet == 0.:

            # If the wing is not symmetric, take only half of the exposed area correction from the reference area

            S_exposed = (seg_Sref -
                         ((chord_root + wing_root) * span_offset * (0.5 * geometry.symmetric)))

            if t_c_w < 0.05:
                seg_Swet = 2.003 * S_exposed
            else:
                seg_Swet = (1.977 + 0.52 * t_c_w) * S_exposed

            geometry.areas.wetted = seg_Swet

        # Calculate upper and lower skin friction compressibility, and Reynolds' number factors

        seg_cf_w_u, seg_k_comp_u, seg_k_reyn_u = compressible_mixed_flat_plate(re_w, Mc, Tc, xtu)
        seg_cf_w_l, seg_k_comp_l, seg_k_reyn_l = compressible_mixed_flat_plate(re_w, Mc, Tc, xtl)

        # Compute airfoil correction
        cos_sweep = np.cos(sweep)

        # Mask for subsonic analysis points
        seg_k_w = np.ones_like(Mc)
        subsonic = Mc <= 1.

        seg_kw[subsonic] = (1.
                            + (2. * C * (t_c_w * cos_sweepv ** 2))
                            / (np.sqrt(1. - (Mc[subsonic] * cos_sweep) ** 2))
                            + ((C * cos_sweep * t_c_w) ** 2 * (1. + 5. * cos_sweep ** 2))
                            / (2. * (1. - (Mc[ind] * cos_sweep) ** 2.)))

        transonic_spline = Cubic_Spline_Blender(.95, 1.0)
        seg_k_w *= transonic_spline.compute(Mc)
        seg_k_w += 1 - transonic_spline.compute(Mc)

        seg_parasite_drag = seg_k_w * seg_Swet / seg_Sref / 2. * (seg_cf_w_u + seg_cf_w_l)

        return (seg_parasite_drag, seg_k_w, seg_cf_w_u, seg_cf_w_l,
                seg_k_comp_u, seg_k_comp_l, seg_k_reyn_u, seg_k_reyn_l, seg_Sref)

    # if wing has segments, compute and sum parasite drag of each segment, else treat it as a single segment

    if len(geometry.Segments.keys()) > 0:
        segments = [s for s in geometry.Segments]
    else:
        segments = [geometry]

    segment_results     = [_single_segmented(segment) for segment in segments]
    total_parasite_drag = np.sum([r[0]*r[8] for r in segment_results])/Sref
    k_w                 = np.sum([r[1]*r[8] for r in segment_results])/Sref
    cf_w_u              = np.sum([r[2]*r[8] for r in segment_results])/Sref
    cf_w_l              = np.sum([r[3]*r[8] for r in segment_results])/Sref
    k_comp_u            = np.sum([r[4]*r[8] for r in segment_results])/Sref
    k_comp_l            = np.sum([r[5]*r[8] for r in segment_results])/Sref
    k_reyn_u            = np.sum([r[6]*r[8] for r in segment_results])/Sref
    k_reyn_l            = np.sum([r[7]*r[8] for r in segment_results])/Sref

    # Dump data to conditions
    wing_result = Data(
        wetted_area=geometry.areas.wetted,
        reference_area=Sref,
        total=total_parasite_drag,
        skin_friction=(cf_w_u + cf_w_l) / 2.,
        compressibility_factor=(k_comp_u + k_comp_l) / 2,
        reynolds_factor=(k_reyn_u + k_reyn_l) / 2,
        form_factor=k_w,
    )
    
    state.conditions.aerodynamics.coefficients.drag.parasite[geometry.tag] = wing_result

    return None
