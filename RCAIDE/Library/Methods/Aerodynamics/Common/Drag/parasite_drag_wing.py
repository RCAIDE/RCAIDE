# RCAIDE/Methods/Aerodynamics/Common/Drag/parasite_drag_wing.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, RCAIDE Team 

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
#TODO: Whole thing is too similar to SUAVE to move over
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
    
     # unpack inputs
    C                             = settings.wing_parasite_drag_form_factor
    recalculate_total_wetted_area = settings.recalculate_total_wetted_area
    freestream                    = state.conditions.freestream
    
    # conditions
    Mc  = freestream.mach_number
    Tc  = freestream.temperature    
    re  = freestream.reynolds_number   
    wing_parasite_drag = 0.0
    
    # Unpack wing
    span_offset  = geometry.percent_span_root_offset
    t_c_w        = geometry.thickness_to_chord
    Sref         = geometry.areas.reference
    num_segments = len(geometry.Segments.keys())
    
    # if wing has segments, compute and sum parasite drag of each segment

    xtu       = geometry.transition_x_upper
    xtl       = geometry.transition_x_lower
    
    if num_segments > 0:
        total_segment_parasite_drag  = 0 
        total_segment_k_w            = 0 
        total_segment_cf_w_u         = 0
        total_segment_cf_w_l         = 0 
        total_segment_k_comp_u       = 0
        total_segment_k_comp_l       = 0
        total_k_reyn_u               = 0          
        total_k_reyn_l               = 0
        
        if recalculate_total_wetted_area:
            geometry = segment_properties(geometry, update_wet_areas=True)
        
        for i, segment in enumerate(geometry.Segments):
            if i == num_segments-1:
                continue  
            mac_seg       = segment.chords.mean_aerodynamic
            Sref_seg      = segment.areas.reference 
            Swet_seg      = segment.areas.wetted
            sweep_seg     = segment.sweeps.quarter_chord
    
            # Parasite drag cf., form factor, skin friction cf., comp. factor and Reynolds number for segments
            (segment_parasite_drag,
             segment_k_w,
             segment_cf_w_u,
             segment_cf_w_l,
             segment_k_comp_u,
             segment_k_comp_l,
             k_reyn_u,
             k_reyn_l) = compute_parasite_drag(re, mac_seg, Mc, Tc, xtu, xtl, sweep_seg, t_c_w, Sref_seg, Swet_seg, C)
            
            total_segment_parasite_drag += segment_parasite_drag * Sref_seg
            total_segment_k_w           += segment_k_w * Sref_seg
            total_segment_cf_w_u        += segment_cf_w_u * Sref_seg
            total_segment_cf_w_l        += segment_cf_w_l * Sref_seg
            total_segment_k_comp_u      += segment_k_comp_u * Sref_seg
            total_segment_k_comp_l      += segment_k_comp_l * Sref_seg
            total_k_reyn_u              += k_reyn_u * Sref_seg
            total_k_reyn_l              += k_reyn_l * Sref_seg
                
        wing_parasite_drag = total_segment_parasite_drag  / Sref
        k_w                = total_segment_k_w / Sref
        cf_w_u             = total_segment_cf_w_u  / Sref
        cf_w_l             = total_segment_cf_w_l / Sref
        k_comp_u           = total_segment_k_comp_u  / Sref
        k_comp_l           = total_segment_k_comp_l  / Sref
        k_reyn_u           = total_k_reyn_u  / Sref
        k_reyn_l           = total_k_reyn_l  / Sref

    # if wing has no segments      
    else:              
        # wing
        mac_w        = geometry.chords.mean_aerodynamic
        sweep_w      = geometry.sweeps.quarter_chord
        span_w       = geometry.spans.projected
        Sref         = geometry.areas.reference
        
        chord_root = geometry.chords.root
        chord_tip  = geometry.chords.tip
        wing_root  = chord_root + span_offset * ((chord_tip - chord_root) / span_w)
        
        if recalculate_total_wetted_area or geometry.areas.wetted == 0.:
            
            # calculate exposed area
            if geometry.symmetric:
                S_exposed_w = geometry.areas.reference - (chord_root + wing_root) * span_offset
            else: 
                S_exposed_w = geometry.areas.reference - 0.5 * (chord_root + wing_root) * span_offset
                
            if t_c_w < 0.05:
                Swet = 2.003 * S_exposed_w
            else:
                Swet = (1.977 + 0.52 * t_c_w) * S_exposed_w
                
            geometry.areas.wetted = Swet
        else:
            Swet = geometry.areas.wetted

        # compute parasite drag coef., form factor, skin friction coef., compressibility factor and reynolds number for wing
        (wing_parasite_drag,
         k_w,
         cf_w_u,
         cf_w_l,
         k_comp_u,
         k_comp_l,
         k_reyn_u,
         k_reyn_l) = compute_parasite_drag(re, mac_w, Mc, Tc, xtu, xtl, sweep_w, t_c_w, Sref, Swet, C)

    # dump data to conditions
    wing_result = Data(
        wetted_area=geometry.areas.wetted,
        reference_area=Sref,
        total=wing_parasite_drag,
        skin_friction=(cf_w_u + cf_w_l) / 2.,
        compressibility_factor=(k_comp_u + k_comp_l) / 2,
        reynolds_factor=(k_reyn_u + k_reyn_l) / 2,
        form_factor=k_w,
    )
    
    state.conditions.aerodynamics.coefficients.drag.parasite[geometry.tag] = wing_result

    return 


# ----------------------------------------------------------------------------------------------------------------------  
#  compute_parasite_drag
# ----------------------------------------------------------------------------------------------------------------------   
def compute_parasite_drag(re,mac_w,Mc,Tc,xtu,xtl,sweep_w,t_c_w,S_ref,Swet,C):
    """Computes the parasite drag due to wings

    Assumptions: 

    Source:
        adg.stanford.edu (Stanford AA241 A/B Course Notes)

    Args:
        re      (float): Reynolds Number                 [unitless]
        mac_w   (float): Wing mean aerodynamic chord     [m]
        Mc      (float): Mach Number                     [unitless]
        Tc      (float): Temperature                     [K]
        xtu     (float): Upper surface transition point  [unitless]  
        xtl     (float): Lower surface transition point  [unitless]  
        sweep_w (float): wing sweep                      [rad]
        t_c_w   (float): wing thickness to chord ratio   [unitless]
        S_ref   (float): wing reference area             [m^2]
        Swet    (float): wing wetted area                [m^2]
        C       (float): form factor                     [unitless]
      
    Returns: 
        wing_parasite_drag  (float): wing parasite drag               [unitless]
        k_w                 (float): form factor                      [unitless]
        cf_w_u              (float): upper skin-friction coefficient  [unitless]
        cf_w_l              (float): lower skin-friction coefficient  [unitless]               
        k_comp_u            (float): upper compressibility factor     [unitless]
        k_comp_l            (float): lower compressibility factor     [unitless]
        k_reyn_u            (float): upper reynolds factor            [unitless]
        k_reyn_l            (float): lower reynolds factor            [unitless]  
    """    
    # reynolds number
    Re_w = re * mac_w
    
    # skin friction  coefficient, upper
    cf_w_u, k_comp_u, k_reyn_u = compressible_mixed_flat_plate(Re_w,Mc,Tc,xtu)
    
    # skin friction  coefficient, lower
    cf_w_l, k_comp_l, k_reyn_l = compressible_mixed_flat_plate(Re_w,Mc,Tc,xtl) 
    
    # correction for airfoils
    cos_sweep   = np.cos(sweep_w)
    cos_squared = cos_sweep*cos_sweep 
    ind         = Mc <= 1. 
    k_w         = np.ones_like(Mc)
    k_w[ind]    = (1.
                   + (2. * C * (t_c_w * cos_squared))
                   / (np.sqrt(1. - Mc[ind] * Mc[ind] * cos_squared))
                   + (C * C * cos_squared * t_c_w * t_c_w * (1. + 5. * cos_squared))
                   / (2. * (1. - (Mc[ind] * cos_sweep) ** 2.)))
    
    spline = Cubic_Spline_Blender(.95,1.0)
    h00    = lambda M: spline.compute(M)
    k_w    = k_w * (h00(Mc)) + 1 * (1 - h00(Mc))
 
    wing_parasite_drag = k_w * Swet / S_ref / 2. * (cf_w_u + cf_w_l)

    return wing_parasite_drag, k_w, cf_w_u, cf_w_l, k_comp_u, k_comp_l, k_reyn_u, k_reyn_l
