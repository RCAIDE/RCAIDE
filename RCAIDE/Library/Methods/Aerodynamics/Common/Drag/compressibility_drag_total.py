# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/compressibility_drag_total.py 
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports   
from RCAIDE.Framework.Core import Data 
from .lift_wave_drag import lift_wave_drag
from .drag_divergence import  drag_divergence 

# legacy imports 
from Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.wave_drag_volume_raymer import wave_drag_volume_raymer
from Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.wave_drag_volume_sears_haack import wave_drag_volume_sears_haack
from Legacy.trunk.S.Methods.Utilities.Cubic_Spline_Blender import Cubic_Spline_Blender

# package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Compressibility Drag Total
# ----------------------------------------------------------------------------------------------------------------------
def compressibility_drag_total(state,settings,geometry):
    """Computes compressibility drag for full aircraft including volume drag

    Assumptions:
        None

    Source:
        None

    Args:
        settings 
            .begin_drag_rise_mach_number                                 (numpy.array): begin_drag_rise_mach_number  [unitless]
            .end_drag_rise_mach_number                                   (numpy.array): end_drag_rise_mach_number    [unitless]
            .peak_mach_number                                            (numpy.array): peak_mach_number             [unitless]
            .transonic_drag_multiplier                                   (numpy.array): transonic_drag_multiplier    [unitless]
            .volume_wave_drag_scaling                                    (numpy.array): volume_wave_drag_scaling     [unitless]
        state.conditions 
            .freestream.mach_number                                      (numpy.array): mach number                  [unitless]
        state.conditions.aerodynamics.coefficients.lift.breakdown
            .compressible_wings                                          (numpy.array): compressible lift for wings  [unitless] 
        geometry
            .maximum_cross_sectional_area                                (numpy.array): maximum_cross_sectional_area [m^2]  
            .total_length                                                (numpy.array): total_length                 [m]    
            .reference_area                                                     (dict): reference_area               [m^2]  
            .wings                                   

    Returns: 
        state.conditions.aerodynamics.coefficients.drag.breakdown             
           .compressible.total                                           (numpy.array): compressible drag            [unitless]
           .compressible.total_volume                                    (numpy.array): compressible drag            [unitless]
           .compressible.total_lift                                      (numpy.array): compressible drag            [unitless]
    """     

    # Unpack 
    low_mach_cutoff  = settings.begin_drag_rise_mach_number
    high_mach_cutoff = settings.end_drag_rise_mach_number
    peak_mach        = settings.peak_mach_number
    peak_factor      = settings.transonic_drag_multiplier
    scaling_factor   = settings.volume_wave_drag_scaling
    
    if settings.wave_drag_type == 'Sears-Haack':
        wave_drag_volume = wave_drag_volume_sears_haack 
    elif settings.wave_drag_type == 'Raymer':
        wave_drag_volume = wave_drag_volume_raymer        
    else:
        raise NotImplementedError   
    if settings.cross_sectional_area_calculation_type != 'Fixed':
        raise NotImplementedError 

    Mc = state.conditions.freestream.mach_number
    cl = state.conditions.aerodynamics.coefficients.lift.breakdown.compressible_wings    
    low_cutoff_volume_total  = np.zeros_like(Mc)
    high_cutoff_volume_total = np.zeros_like(Mc)
    cd_c_v                   = np.zeros_like(Mc) 
     
    for wing in geometry.wings:
        low_cutoff_volume_total += drag_divergence(low_mach_cutoff, wing, cl[wing.tag], geometry.reference_area)[0]
    high_cutoff_volume_total = wave_drag_volume(geometry,low_mach_cutoff,scaling_factor) 
    peak_volume_total = high_cutoff_volume_total*peak_factor
    
    # subsonic and supersonic coefficients 
    a1 = (low_cutoff_volume_total-peak_volume_total)/(low_mach_cutoff-peak_mach)/(low_mach_cutoff-peak_mach) 
    a2 = (high_cutoff_volume_total-peak_volume_total)/(high_mach_cutoff-peak_mach)/(high_mach_cutoff-peak_mach)
    
    # parabolic approximation of drag rise in the transonic region
    def CD_visc_func(M,a_vertex): 
        ret = a_vertex*(M-peak_mach)*(M-peak_mach)+peak_volume_total
        ret = ret.reshape(np.shape(M))
        return ret
    
    # Cubic Hermite spline
    sub_spline  = Cubic_Spline_Blender(low_mach_cutoff, peak_mach- 3/4*(peak_mach-low_mach_cutoff))
    sup_spline  = Cubic_Spline_Blender(peak_mach,high_mach_cutoff)
    sub_h00     = lambda M:sub_spline.compute(M)
    sup_h00     = lambda M:sup_spline.compute(M)  
    low_inds    = Mc[:,0]<peak_mach
    hi_inds     = Mc[:,0]>=peak_mach 
    
    cd_c_v_base = np.zeros_like(Mc)    
    for wing in geometry.wings:
        cd_c_v_base[low_inds] += drag_divergence(Mc[low_inds], wing, cl[wing.tag][low_inds], geometry.reference_area)[0] 
    cd_c_v_base[Mc>=peak_mach] = wave_drag_volume(geometry, Mc[Mc>=peak_mach], scaling_factor)  
    cd_c_v[low_inds]           = cd_c_v_base[low_inds]*(sub_h00(Mc[low_inds])) + CD_visc_func(Mc[low_inds],a1[low_inds])*(1-sub_h00(Mc[low_inds]))
    cd_c_v[hi_inds]            = CD_visc_func(Mc[hi_inds],a2)*(sup_h00(Mc[hi_inds])) + cd_c_v_base[hi_inds]*(1-sup_h00(Mc[hi_inds])) 
    cd_c_l_base                = lift_wave_drag(state.conditions, geometry.wings.main_wing, geometry.reference_area)
    cd_c_l                     = cd_c_l_base*(1-sup_h00(Mc)) 
    cd_c                       = cd_c_v + cd_c_l 

    # Store resu
    state.conditions.aerodynamics.coefficients.drag.breakdown.compressible              = Data() 
    state.conditions.aerodynamics.coefficients.drag.breakdown.compressible.total        = cd_c
    state.conditions.aerodynamics.coefficients.drag.breakdown.compressible.total_volume = cd_c_v
    state.conditions.aerodynamics.coefficients.drag.breakdown.compressible.total_lift   = cd_c_l
    
    return cd_c
