# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/form_drag.py 
# 
# Created:  Jul 2025, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
  
from RCAIDE.Framework.Core   import Units 
from scipy.interpolate       import RegularGridInterpolator

# package imports
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
#  Form Drag 
# ----------------------------------------------------------------------------------------------------------------------   
def form_drag(state,settings,geometry):
    """Computes the form drag associated with an aircraft  
    """ 

    conditions  = state.conditions   
    Mach        = conditions.freestream.mach_number 
    alpha       = conditions.aerodynamics.angles.alpha   
    
    CD_form_total = np.zeros_like(Mach) 
    # use simple form drag estimate  
    #CD_form      =   Mach*(107.9 * (alpha**4) - 17.888 * (alpha**3) + 2.2026 * (alpha**2) + 0.0512 * (alpha) - 0.0021) 
    #CD_form[Mach>1]  = 0
    #CD_form_total    += CD_form * (wing.areas.reference / geometry.reference_area)
            
    state.conditions.aerodynamics.coefficients.drag.form.total = CD_form_total 
    return  

def compute_wing_form_drag(conditions,inboard_airfoil_polar, outboard_airfoil_polar,aspect_ratio, S_ref,span,root_chord,tip_chord,root_twist,tip_twist,sweep_le,n):

    alpha       = conditions.aerodynamics.angles.alpha
    non_dim_Re  = conditions.freestream.reynolds_number   
    n_cases =  len(alpha)
    
    # get dimensional reynolds number                     
    segment_chords         = np.linspace(root_chord,tip_chord,n)
    chord_Res              = segment_chords * non_dim_Re 

    eta                    = np.linspace(0,1,n) 
    twist_distribution     = np.tile(np.linspace(root_twist,tip_twist,n)[None,:] ,(n_cases,1)) 
    AoA_eff                = alpha + twist_distribution 

    # function for converting 2D polars into 3D polars considering the effect of sweep and boundary layer growth 
    kappa_tip              = aspect_ratio * (eta)
    kappa_root             = aspect_ratio * (eta - 1)
    kappa                  = 1 +  kappa_root  +  kappa_tip  
    sweep_eff              = sweep_le * kappa
    F_sweep                = np.cos(sweep_eff)

    # determine the angle of attack at zero lift
    AoAs                   = np.linspace(-14,90,105)*Units.degrees 
    inboard_idx            = np.argmin(abs(inboard_airfoil_polar.lift_coefficients), axis=1)
    outboard_idx           = np.argmin(abs(outboard_airfoil_polar.lift_coefficients), axis=1)
    inboard_AoA_0s         = AoAs[inboard_idx]
    outboard_AoA_0s        = AoAs[outboard_idx] 
    inboard_AoA_0          = np.interp(chord_Res,inboard_airfoil_polar.reynolds_numbers,inboard_AoA_0s)
    outboard_AoA_0         = np.interp(chord_Res,inboard_airfoil_polar.reynolds_numbers,outboard_AoA_0s)

    # update angle of attack to consider sweep 
    inboard_AoA_2_5_D      = (AoA_eff - inboard_AoA_0) * F_sweep +  inboard_AoA_0 
    outboard_AoA_2_5_D     = (AoA_eff - outboard_AoA_0) * F_sweep +  outboard_AoA_0

    # compute 2.5 D effective Cl and CDs for the two sections use linear blending for CLs between section breaks 
    inboard_Cdrag_func     = RegularGridInterpolator((inboard_airfoil_polar.reynolds_numbers, inboard_airfoil_polar.angle_of_attacks),inboard_airfoil_polar.drag_coefficients       ,method = 'nearest',   bounds_error=False, fill_value=None)
    outboard_Cdrag_func    = RegularGridInterpolator((outboard_airfoil_polar.reynolds_numbers, outboard_airfoil_polar.angle_of_attacks),outboard_airfoil_polar.drag_coefficients       ,method = 'nearest',   bounds_error=False, fill_value=None)

    inboard_pts            = np.hstack((chord_Res.reshape(n_cases * n , 1),inboard_AoA_2_5_D.reshape(n_cases * n , 1))) 
    outboard_pts           = np.hstack((chord_Res.reshape(n_cases * n, 1),outboard_AoA_2_5_D.reshape(n_cases * n , 1))) 
    inboard_Cdrag_eff_i    = np.atleast_2d(inboard_Cdrag_func(inboard_pts)).reshape(n_cases, n  )
    outboard_Cdrag_eff_i   = np.atleast_2d(outboard_Cdrag_func(outboard_pts)).reshape(n_cases, n )
 
    CD_form_y              = inboard_Cdrag_eff_i* (1- eta)  + outboard_Cdrag_eff_i*eta 
    spacing                = np.linspace(0,1,n+1)  
    delta_y                = np.diff(spacing * span)
    D_form_wing            = np.atleast_2d(np.sum(CD_form_y  * segment_chords * delta_y, axis=1)).T 
    CD_form_wing           = D_form_wing /(S_ref)
    
    return CD_form_wing