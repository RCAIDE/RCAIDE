# RCAIDE/Library/Methods/Aerodynamics/Athena_Vortex_Lattice/build_VLM_surrogates.py
#
# Created: Oct 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# package imports 
from scipy.interpolate                                           import RegularGridInterpolator 

# ----------------------------------------------------------------------------------------------------------------------
#  build_AVL_surrogates
# ---------------------------------------------------------------------------------------------------------------------- 
def build_AVL_surrogates(aerodynamics):
    """Build a surrogate using sample evaluation results.
    
    Assumptions:
        None
        
    Source:
        None

    Args:
        aerodynamics       : VLM analysis          [unitless] 
        
    Returns: 
        None  
    """
    surrogates  = aerodynamics.surrogates
    training    = aerodynamics.training  
    AoA_data    = training.angle_of_attack
    mach_data   = training.Mach 
 
    surrogates.Clift_spanwise              = RegularGridInterpolator((AoA_data, mach_data), training.CL_y        ,method='linear',    bounds_error=False, fill_value=None)    
    surrogates.lift_coefficient            = RegularGridInterpolator((AoA_data, mach_data), training.CL          ,method = 'linear',   bounds_error=False, fill_value=None)   
    surrogates.drag_coefficient            = RegularGridInterpolator((AoA_data, mach_data), training.CDi         ,method = 'linear',   bounds_error=False, fill_value=None)   
    surrogates.span_efficiency_factor      = RegularGridInterpolator((AoA_data, mach_data), training.CM          ,method = 'linear',   bounds_error=False, fill_value=None)   
    surrogates.moment_coefficient          = RegularGridInterpolator((AoA_data, mach_data), training.e           ,method = 'linear',   bounds_error=False, fill_value=None)   
    surrogates.Cm_alpha_moment_coefficient = RegularGridInterpolator((AoA_data, mach_data), training.Cm_alpha    ,method = 'linear',   bounds_error=False, fill_value=None)    
    surrogates.Cn_beta_moment_coefficient  = RegularGridInterpolator((AoA_data, mach_data), training.Cn_beta     ,method = 'linear',   bounds_error=False, fill_value=None)   
    surrogates.neutral_point               = RegularGridInterpolator((AoA_data, mach_data), training.NP          ,method = 'linear',   bounds_error=False, fill_value=None)         
        
    return 