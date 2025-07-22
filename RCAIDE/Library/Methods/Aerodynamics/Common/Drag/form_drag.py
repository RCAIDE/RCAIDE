# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/form_drag.py 
# 
# Created:  Jul 2025, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
  
from RCAIDE.Framework.Core                    import Data ,  Units
from RCAIDE.Library.Methods.Geometry.Airfoil  import compute_naca_4series 
from RCAIDE.Library.Methods.Aerodynamics.Airfoil_Panel_Method.airfoil_analysis      import airfoil_analysis
from scipy.interpolate   import RegularGridInterpolator
# package imports
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
#  Form Drag 
# ----------------------------------------------------------------------------------------------------------------------   
def form_drag(state,settings,geometry):
    """Computes the form drag associated with an aircraft
 

    Returns: 
    """ 

    conditions  = state.conditions   
    b_ref       = state.analyses.aerodynamics.reference_values.b_ref
    S_ref       = state.analyses.aerodynamics.reference_values.S_ref
    Mach        = conditions.freestream.mach_number 
    alpha       = conditions.aerodynamics.angles.alpha
    Re          = conditions.freestream.reynolds_number
    n_cases     = len(alpha) 
     

    # ------------------------------------------------------------------------------------------
    # Form Drag 
    # ------------------------------------------------------------------------------------------ 
    #LE_ind     = settings.vortex_distribution.leading_edge_indices 
    #CHORD      = settings.vortex_distribution.chord_lengths[0,:] 
    #n_sw       = settings.vortex_distribution.n_sw
    #CDrag_f_y = np.zeros((n_cases,len(CHORD[LE_ind])))  
    #non_dim_Re = np.tile(Re, (1, len(CHORD[LE_ind]) ))
    
    
    CD_form_total = np.zeros_like(Mach)
    for wing in geometry.wings:
        if wing.vertical == False:
            if len(wing.segments) > 0: 
                for segment in wing.segments:
                    if segment.airfoil_2D_polars:
                        # use polars 
                        CD_form  = 0 
                    else:
                        # use simple form drag estimate
                        CD_form  = 2.5633 * (alpha**2) - 0.0411 * alpha - 0.0053
                        
                    CD_form[alpha<0.055] = alpha[alpha<0.055] 
                    CD_form_total += CD_form* (segment.areas.reference / geometry.reference_area)
            else:
                if wing.airfoil_2D_polars:
                    # use polars 
                    CD_form = 0
                else:
                    # use simple form drag estimate 
                    CD_form  = 2.5633 * (alpha**2) - 0.0411 * alpha - 0.0053
                    CD_form[alpha<0.055] = alpha[alpha<0.055]
                CD_form_total += CD_form * (wing.areas.reference / geometry.reference_area)
            
            
    #ws = 0  
    #counter = 0
    #for w_i, wing in enumerate(settings.vortex_distribution.VLM_wings): 
        #for seg_i in range(len(wing.seg_breaks) - 1): 
            #ws_prev = ws
            #ws      += n_sw[counter]                
             
            ## get polar at section break
            #inboard_airfoil_polar  = wing.seg_breaks[seg_i].airfoil.polars
            #outboard_airfoil_polar = wing.seg_breaks[seg_i+1].airfoil.polars 

            ## get dimensional reynolds number                     
            #segment_chords         = np.tile(CHORD[ws_prev:ws],(n_cases,1))
            #chord_Res              = segment_chords * non_dim_Re[:,ws_prev:ws]

            #linear_smoothing       = np.tile(np.linspace(0,1,n_sw[counter])[None,:],(n_cases , 1)) 
            ##AoA_eff                = alpha[:,ws_prev:ws] 
            #twist_distribution     = np.tile(np.linspace(wing.seg_breaks[seg_i].twist, wing.seg_breaks[seg_i+1].twist,n_sw[counter])[None,:] ,(n_cases,1)) 
            #AoA_eff                = alpha[:,ws_prev:ws] + twist_distribution #  - delta_alpha_induced[:,ws_prev:ws]             

            ## function for converting 2D polars into 3D polars considering the effect of sweep and boundary layer growth 
            #eta                    =  2 * np.tile(VD.YC[ws_prev:ws][None,:],(n_cases , 1))/b_ref
            #kappa_tip              =  wing.aspect_ratio * (eta)
            #kappa_root             =  wing.aspect_ratio * (eta - 1)
            #kappa                  =  1 +  kappa_root  +  kappa_tip  
            #sweep_eff              =  wing.seg_breaks[seg_i].sweep_outboard_LE * kappa
            #F_sweep                =  np.cos(sweep_eff)
            
            ## determine the angle of attack at zero lift
            #AoAs                   = np.linspace(-14,90,105)*Units.degrees 
            #inboard_idx            = np.argmin(abs(inboard_airfoil_polar.lift_coefficients), axis=1)
            #outboard_idx           = np.argmin(abs(outboard_airfoil_polar.lift_coefficients), axis=1)
            #inboard_AoA_0s         = AoAs[inboard_idx]
            #outboard_AoA_0s        = AoAs[outboard_idx] 
            #inboard_AoA_0          = np.interp(chord_Res,inboard_airfoil_polar.reynolds_numbers,inboard_AoA_0s)
            #outboard_AoA_0         = np.interp(chord_Res,inboard_airfoil_polar.reynolds_numbers,outboard_AoA_0s)
             
            ## update angle of attack to consider sweep 
            #inboard_AoA_2_5_D      = (AoA_eff - inboard_AoA_0) * F_sweep +  inboard_AoA_0 
            #outboard_AoA_2_5_D     = (AoA_eff - outboard_AoA_0) * F_sweep +  outboard_AoA_0
                                
            ## compute 2.5 D effective Cl and CDs for the two sections use linear blending for CLs between section breaks

            #inboard_Cdrag_func     = RegularGridInterpolator((inboard_airfoil_polar.reynolds_numbers, inboard_airfoil_polar.angle_of_attacks),inboard_airfoil_polar.drag_coefficients       ,method = 'nearest',   bounds_error=False, fill_value=None)
            #outboard_Cdrag_func    = RegularGridInterpolator((outboard_airfoil_polar.reynolds_numbers, outboard_airfoil_polar.angle_of_attacks),outboard_airfoil_polar.drag_coefficients       ,method = 'nearest',   bounds_error=False, fill_value=None)
            
            #inboard_pts            = np.hstack((chord_Res.reshape(num_cp * n_sw[counter]      , 1),inboard_AoA_2_5_D.reshape(num_cp *  n_sw[counter]      , 1))) 
            #outboard_pts           = np.hstack((chord_Res.reshape(num_cp * n_sw[counter]      , 1),outboard_AoA_2_5_D.reshape(num_cp * n_sw[counter]      , 1))) 
            #inboard_Cdrag_eff_i    = np.atleast_2d(inboard_Cdrag_func(inboard_pts)).reshape(num_cp, n_sw[counter]      )
            #outboard_Cdrag_eff_i   = np.atleast_2d(outboard_Cdrag_func(outboard_pts)).reshape(num_cp, n_sw[counter]      ) 
            #CDrag_f_y[:,ws_prev:ws] = inboard_Cdrag_eff_i* (1- linear_smoothing)  + outboard_Cdrag_eff_i*linear_smoothing             
      
    #state.conditions.aerodynamics.coefficients.drag.form.total = CD_form_total 
    return  
    