# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/form_drag.py 
# 
# Created:  Jul 2025, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
  
from RCAIDE.Framework.Core                    import Data ,  Units
from RCAIDE.Library.Methods.Geometry.Airfoil  import compute_naca_4series
from RCAIDE.Framework.Core import interp2d 
from RCAIDE.Library.Methods.Aerodynamics.Airfoil_Panel_Method.airfoil_analysis      import airfoil_analysis
# package imports
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
#  Form Drag Total
# ----------------------------------------------------------------------------------------------------------------------   
def form_drag(state,settings,geometry):
    """Computes the form drag associated with an aircraft
 

    Returns: 
    """ 

    conditions     = state.conditions  
    S_ref          = geometry.reference_area
    Mach           = conditions.freestream.mach_number 
   
    # generate vortex distribution (VLM steps 1-9)
    VD   = 0 

    # unpack geometry----------------------------------------------------------------
    S_ref      = geometry.reference_area              
 
    if 'main_wing' in geometry.wings:
        c_bar      = geometry.wings['main_wing'].chords.mean_aerodynamic
        x_mac      = geometry.wings['main_wing'].aerodynamic_center[0] + geometry.wings['main_wing'].origin[0][0]
        z_mac      = geometry.wings['main_wing'].aerodynamic_center[2] + geometry.wings['main_wing'].origin[0][2]
        b_ref      = geometry.wings['main_wing'].spans.projected
    else:
        c_bar  = 0.
        x_mac  = 0.
        b_ref = 0.
        for wing in geometry.wings:
            if wing.vertical == False:
                if c_bar <= wing.chords.mean_aerodynamic:
                    c_bar  = wing.chords.mean_aerodynamic
                    x_mac  = wing.aerodynamic_center[0] + wing.origin[0][0]
                    z_mac  = wing.aerodynamic_center[2] + wing.origin[0][2]
                    b_ref  = wing.spans.projected

    x_cg       = geometry.mass_properties.center_of_gravity[0][0]
    z_cg       = geometry.mass_properties.center_of_gravity[0][2]
    if x_cg == 0.0:
        x_m = x_mac 
        z_m = z_mac
    else:
        x_m = x_cg
        z_m = z_cg    

    # create arrays of delta_alpha_i for each strip

    LE_ind               = VD.leading_edge_indices 
    CHORD                = VD.chord_lengths[0,:]
    delta_alpha_induced  = np.repeat(conditions.aerodynamics.angles.alpha*0, VD.n_cp, axis = 1)
    
    num_cp = len(conditions.aerodynamics.angles.alpha)
    Cdrag_eff_i               = np.zeros((num_cp,len(CHORD[LE_ind])))
    Clift_eff_i               = np.zeros((num_cp,len(CHORD[LE_ind])))
    Clift_y_visc              = np.zeros((num_cp,len(CHORD[LE_ind])))
    error_diff                 =  1
 
    non_dim_Re = np.tile(conditions.freestream.reynolds_number, (1, len(CHORD[LE_ind]) ))
    AoA        =  np.tile(conditions.aerodynamics.angles.alpha , (1, len(CHORD[LE_ind]) ))
    
   
    for w_i, wing in enumerate(VD.VLM_wings):
        
        for seg_i in range(len(wing.seg_breaks) - 1):

            ws_prev = ws
            ws         += n_sw[counter]                
             
            # get polar at section break
            inboard_airfoil_polar  = wing.seg_breaks[seg_i].airfoil.polars
            outboard_airfoil_polar = wing.seg_breaks[seg_i+1].airfoil.polars 

            # get dimensional reynolds number                     
            segment_chords         = np.tile(CHORD[ws_prev:ws],(num_cp,1))
            chord_Res              = segment_chords * non_dim_Re[:,ws_prev:ws]

            linear_smoothing       = np.tile(np.linspace(0,1,n_sw[counter])[None,:],(num_cp , 1))
            twist_distribution     = np.tile(np.linspace(wing.seg_breaks[seg_i].twist, wing.seg_breaks[seg_i+1].twist,n_sw[counter])[None,:] ,(num_cp,1)) 
            AoA_eff                = AoA[:,ws_prev:ws] # - twist_distribution - delta_alpha_induced[:,ws_prev:ws] 

            # function for converting 2D polars into 3D polars considering the effect of sweep and boundary layer growth 
            eta                    =  2 * np.tile(VD.YC[ws_prev:ws][None,:],(num_cp , 1))/b_ref
            kappa_tip              =  wing.aspect_ratio * (eta)
            kappa_root             =  wing.aspect_ratio * (eta - 1)
            kappa                  =  1 +  kappa_root  +  kappa_tip  
            sweep_eff              =  wing.seg_breaks[seg_i].sweep_outboard_LE * kappa
            F_sweep                =  np.cos(sweep_eff)
            
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
            inboard_Clift_eff_i    = interp2d(chord_Res,inboard_AoA_2_5_D,inboard_airfoil_polar.reynolds_numbers, inboard_airfoil_polar.angle_of_attacks, inboard_airfoil_polar.lift_coefficients)
            inboard_Cdrag_eff_i    = interp2d(chord_Res,inboard_AoA_2_5_D,inboard_airfoil_polar.reynolds_numbers, inboard_airfoil_polar.angle_of_attacks, inboard_airfoil_polar.drag_coefficients)
            outboard_Clift_eff_i   = interp2d(chord_Res,outboard_AoA_2_5_D,outboard_airfoil_polar.reynolds_numbers, outboard_airfoil_polar.angle_of_attacks, outboard_airfoil_polar.lift_coefficients)
            outboard_Cdrag_eff_i   = interp2d(chord_Res,outboard_AoA_2_5_D,outboard_airfoil_polar.reynolds_numbers, outboard_airfoil_polar.angle_of_attacks, outboard_airfoil_polar.drag_coefficients)
            Cdrag_eff_i[:,ws_prev:ws] = inboard_Cdrag_eff_i* (1- linear_smoothing)  + outboard_Cdrag_eff_i*linear_smoothing  
            Clift_eff_i[:,ws_prev:ws] = (inboard_Clift_eff_i* (1- linear_smoothing)  + outboard_Clift_eff_i*linear_smoothing ) * (F_sweep ** 2)
      
    
    return  
    
def form_drag_surrogate(self):
    
    # Batch analysis of single airfoil - NACA 4412  
    AoA_deg              = np.linspace(-5,10,16)
    Res                  = np.array([1E4, 1E5, 1E6, 1E7]) 
    
    CDs = np.zeros((len(Re_vals), len(AoA_deg))) 
    for i in range(len(Re_vals)):
    
        Re_vals              = np.atleast_2d(np.ones(len(AoA_deg)))*Res[i]     
        AoA_rad              = np.atleast_2d(AoA_deg*Units.degrees)   
        airfoil_file_1       = '4412'
        airfoil_geometry_1   = compute_naca_4series(airfoil_file_1,npoints = 201)
        airfoil_properties_1 = airfoil_analysis(airfoil_geometry_1,AoA_rad,Re_vals) 
        CDs[ i, :] = airfoil_properties_1.cd_visc 
    
    return CDs