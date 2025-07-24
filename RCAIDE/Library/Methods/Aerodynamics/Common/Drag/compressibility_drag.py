# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/compressibility_drag_total.py
# 
# Created:  Jul 2024, RCAIDE Team 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from RCAIDE.Framework.Core                    import Data
from RCAIDE.Library.Components.Wings          import Main_Wing
from RCAIDE.Library.Methods.Utilities         import Cubic_Spline_Blender
from .drag_divergence                         import drag_divergence  

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
    Cl               = conditions.aerodynamics.coefficients.lift.total   
    low_mach_cutoff  = settings.supersonic.begin_drag_rise_mach_number 
    peak_mach        = settings.supersonic.peak_mach_number 
   
    sub_spline = Cubic_Spline_Blender(low_mach_cutoff, peak_mach-(peak_mach-low_mach_cutoff)*3/4) 
    sub_h00    = lambda M:sub_spline.compute(M)  
    low_inds   = Mach[:,0]<peak_mach 

    cd_compressibility           = np.zeros_like(Mach) 
    cd_compressibility[low_inds] = drag_divergence(Mach[low_inds], geometry,Cl[low_inds])  
    
    cd_c           = np.zeros_like(Mach)
    cd_c[low_inds] = cd_compressibility[low_inds]*(sub_h00(Mach[low_inds]))   
  
    # ---------------------------------------------------------------------     
    # total compressibility drag
    # --------------------------------------------------------------------- 
    conditions.aerodynamics.coefficients.drag.compressible = Data(total   = cd_c)  
        
    return  