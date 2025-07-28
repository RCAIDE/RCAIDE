# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/compressibility_drag.py
# 
# Created:  Jul 2024, RCAIDE Team 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
from RCAIDE.Library.Methods.Utilities         import Cubic_Spline_Blender 

# package imports
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
#  Compressibility Drag Total
# ----------------------------------------------------------------------------------------------------------------------  
def compressibility_drag(state,settings,geometry):
    """Computes compressibility drag for full aircraft including volume drag

    Assumptions:
    None

    Source:
    None

    Args:   
    settings.
      begin_drag_rise_mach_number                                    [Unitless]
      end_drag_rise_mach_number                                      [Unitless]
      peak_mach_number                                               [Unitless]
      transonic_drag_multiplier                                      [Unitless]
      volume_wave_drag_scaling                                       [Unitless]
    state.conditions.freestream.mach_number                          [Unitless]
    geometry.maximum_cross_sectional_area                            [m^2] (used in subfunctions)
    geometry.total_length                                            [m]   (used in subfunctions)
    geometry.reference_area                                          [m^2]
    geometry.wings                             

    Returns:
    total_compressibility_drag                                       [Unitless]

    Properties Used:
    None
    """     

    # Unpack
    conditions       = state.conditions
    Mach             = conditions.freestream.mach_number  
    low_mach_cutoff  = settings.supersonic.begin_drag_rise_mach_number 
    peak_mach        = settings.supersonic.peak_mach_number 

    sub_spline = Cubic_Spline_Blender(low_mach_cutoff, peak_mach-(peak_mach-low_mach_cutoff)*3/4) 
    sub_h00    = lambda M:sub_spline.compute(M)  
    low_inds   = Mach[:,0]<peak_mach   

    cd_compressibility  = np.zeros_like(Mach)  
    for wing in  geometry.wings:  
        sweep_w   = wing.sweeps.leading_edge 

        # Get effective CLift_wings and sweep
        tc = wing.thickness_to_chord / np.cos(sweep_w)
        cl = conditions.aerodynamics.coefficients.lift.inviscid.wings[wing.tag]/ (np.cos(sweep_w) ** 2)

        # Compressibility drag based on regressed fits from AA241 
        mcc_cos_ws = 0.922321524499352       \
                - 1.153885166170620*tc    \
                       - 0.304541067183461*cl    \
                       + 0.332881324404729*tc*tc \
                       + 0.467317361111105*tc*cl \
                       + 0.087490431201549*cl*cl

        # Crest-critical Mach number, corrected for wing sweep
        Mcc = mcc_cos_ws/ np.cos(sweep_w)      

        # Divergence ratio
        mo_Mach = Mach/Mcc

        # Compressibility correlation, Shevell
        dcdc_cos3g = 0.0019*mo_Mach**14.641

        # Compressibility drag  
        cd_c = dcdc_cos3g * (np.cos(sweep_w)**3) 
         
        cd_compressibility += cd_c * (wing.areas.reference / geometry.reference_area)  
 
    cd_compressibility[low_inds] = cd_compressibility[low_inds]*(sub_h00(Mach[low_inds]))   
   
    # store results  
    conditions.aerodynamics.coefficients.drag.compressible.total = cd_compressibility

    return  