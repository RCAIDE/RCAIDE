## @ingroup Methods-Flight_Dynamics-Static_Stability
# compute_aero_derivatives.py
# 
# Created:   Aug 2021, R. Erhard
# Modified: 
# Nov 2022, D. Enriquez - added Cdrag_alpha, CY_beta
# Mar 2024, M. Guidotti - added analytical compuation of derivatives of latero-directional stability
# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import numpy as np 
from copy import deepcopy


## @ingroup Methods-Flight_Dynamics-Static_Stability
def compute_aero_derivatives_lateral(conditions): 
    """This function computes the longitudinal aerodynamic derivatives of the aircraft about a 
    mission segment, and stores them in the aero_derivatives data structure associated
    with the state conditions of the given mission segment. All derivatives are 
    computed using forward difference.
    
    Assumptions:
       Linearized equations are used for each state variable

    Source:
      N/A

    Inputs:
      segment                SUAVE mission segment
      
    Outputs: 
       segment.state.conditions.aero_derivatives
         .Clift_alpha       -   lift-curve slope                                                            [-]  
         .Cdrag_alpha       -   derivative of inviscid drag with respect to angle of attack                 [-]
         .dCM_dAlpha       -   derivative of pitching moment coefficient with respect to angle of attack   [-] 
         .dCT_dAlpha       -   derivative of rotor thrust coefficient with respect to angle of attack      [-] 
         .dCP_dAlpha       -   derivative of rotor power coefficient with respect to angle of attack       [-] 
         .dCL_dThrottle    -   derivative of lift coefficient with respect to throttle                     [-] 
         .dCD_dThrottle    -   derivative of drag coefficient with respect to throttle                     [-] 
         .dCT_dThrottle    -   derivative of rotor thrust coefficient with respect to throttle             [-] 
         .dCP_dThrottle    -   derivative of rotor power coefficient with respect to throttle              [-] 
           

    Properties Used:
       N/A
     """
    ## check for surrogate
    #surrogate_used = segment.analyses.aerodynamics.settings.use_surrogate
    
    ## extract states from converged mission segment
    #orientation_vector = segment.state.conditions.frames.body.inertial_rotations
    
    #pitch     = orientation_vector[:,1]
    #psi       = orientation_vector[:,2]      # heading 
    #throttle  = segment.state.conditions.propulsion.throttle
    
    #n_cpts    = len(pitch)
    
    ## ----------------------------------------------------------------------------
    ## Perturb each state variable
    ## ----------------------------------------------------------------------------
    #h = 1e-4
    ## ----------------------------------------------------------------------------    
    ## Alpha perturbation
    
    #perturbed_segment = deepcopy(segment)    
    #pitch_plus        = pitch*(1+h)
    #perturbed_segment.state.conditions.frames.body.inertial_rotations[:,1] = pitch_plus
    
    #iterate = perturbed_segment.process.iterate
    #iterate.conditions(perturbed_segment) 
    
    ## set segment derivatives based on perturbed segment
    #dAlpha = perturbed_segment.state.conditions.aerodynamics.angle_of_attack - segment.state.conditions.aerodynamics.angle_of_attack
    #dCL    = perturbed_segment.state.conditions.aerodynamics.lift_coefficient - segment.state.conditions.aerodynamics.lift_coefficient
    #dCD    = perturbed_segment.state.conditions.aerodynamics.drag_coefficient - segment.state.conditions.aerodynamics.drag_coefficient #DE added
    
    #if surrogate_used:
        #dCM_dAlpha = segment.state.conditions.static_stability.Cm_alpha
    #else:
        ## use VLM outputs directly
        #dCM    = perturbed_segment.state.conditions.aerodynamics.moment_coefficient - segment.state.conditions.aerodynamics.moment_coefficient
        #dCM_dAlpha = dCM/dAlpha
        
    ## propeller derivatives
    #dCT, dCP = propeller_derivatives(segment, perturbed_segment, n_cpts)
        
    #Clift_alpha = dCL/dAlpha
    #Cdrag_alpha = dCD/dAlpha
    #dCT_dAlpha = dCT/dAlpha[None,:,:]
    #dCP_dAlpha = dCP/dAlpha[None,:,:]
    
    #segment.state.conditions.aero_derivatives.Clift_alpha = Clift_alpha
    #segment.state.conditions.aero_derivatives.Cdrag_alpha = Cdrag_alpha
    #segment.state.conditions.aero_derivatives.dCM_dAlpha = dCM_dAlpha
    #segment.state.conditions.aero_derivatives.dCT_dAlpha = dCT_dAlpha
    #segment.state.conditions.aero_derivatives.dCP_dAlpha = dCP_dAlpha
    
    
    ## ----------------------------------------------------------------------------    
    ## Beta perturbation
    
    #perturbed_segment = deepcopy(segment)    
    #psi_plus          = psi+h
    #perturbed_segment.state.conditions.frames.body.inertial_rotations[:,2] = psi_plus
    
    #iterate = perturbed_segment.process.iterate
    #iterate.conditions(perturbed_segment) 
    
    ## set segment derivatives based on perturbed segment
    #dBeta  = perturbed_segment.state.conditions.aerodynamics.sideslip_angle - segment.state.conditions.aerodynamics.sideslip_angle
    
    ## roll and yaw moment coefficient derivatives
    #if surrogate_used:
        ## check for roll and yaw moment coefficient derivatives in surrogate outputs
        #if 'Cn_beta' in segment.state.conditions.static_stability.keys():
            #CN_beta = segment.state.conditions.static_stability.Cn_beta
        #else:
            #print("No CN_beta in surrogate output. CN_beta not included in aerodynamic derivatives.")
            #CN_beta = None
        #if 'Cl_beta' in segment.state.conditions.static_stability.keys():
            #CL_beta = segment.state.conditions.static_stability.Cl_beta 
        #else:
            #print("No CL_beta in surrogate output. CL_beta not included in aerodynamic derivatives.")
            #CL_beta = None 
            
        #if 'CY_beta' in segment.state.conditions.static_stability.keys():
            #CY_beta = segment.state.conditions.static_stability.CY_beta 
        #else:
            #print("No CY_beta in surrogate output. CY_beta not included in aerodynamic derivatives.")
            #CY_beta = None
    #else:
        ## use VLM outputs directly
        #dCn = perturbed_segment.state.conditions.static_stability.yawing_moment_coefficient - segment.state.conditions.static_stability.yawing_moment_coefficient
        #dCl = perturbed_segment.state.conditions.static_stability.rolling_moment_coefficient - segment.state.conditions.static_stability.rolling_moment_coefficient
        #dCY = perturbed_segment.state.conditions.aerodynamics.side_force_coefficient - segment.state.conditions.aerodynamics.side_force_coefficient 
        #CN_beta = dCn/dBeta
        #CL_beta = dCl/dBeta
        #CY_beta = dCY/dBeta 
        
    ## check for propellers
    #dCT, dCP = propeller_derivatives(segment, perturbed_segment, n_cpts)  

    #dCT_dBeta = dCT/dBeta
    #dCP_dBeta = dCP/dBeta
    
    #segment.state.conditions.aero_derivatives.CN_beta = CN_beta
    #segment.state.conditions.aero_derivatives.CL_beta = CL_beta
    #segment.state.conditions.aero_derivatives.CY_beta = CY_beta 
    #segment.state.conditions.aero_derivatives.dCT_dBeta = dCT_dBeta
    #segment.state.conditions.aero_derivatives.dCP_dBeta = dCP_dBeta
    
    
    ## ----------------------------------------------------------------------------    
    ## Throttle perturbation
    
    #perturbed_segment = deepcopy(segment)    
    #throttle_plus     = throttle*(1+h)
    #perturbed_segment.state.conditions.propulsion.throttle = throttle_plus
    
    #iterate = perturbed_segment.process.iterate
    #iterate.conditions(perturbed_segment) 
    
    ## set segment derivatives based on perturbed segment
    #dThrottle = throttle_plus-throttle
    #dCL       = perturbed_segment.state.conditions.aerodynamics.lift_coefficient - segment.state.conditions.aerodynamics.lift_coefficient
    #dCD       = perturbed_segment.state.conditions.aerodynamics.drag_coefficient - segment.state.conditions.aerodynamics.drag_coefficient

    ## check for propellers
    #dCT, dCP = propeller_derivatives(segment, perturbed_segment, n_cpts)  

    #dCL_dThrottle = dCL/dThrottle
    #dCD_dThrottle = dCD/dThrottle
    #dCT_dThrottle = dCT/dThrottle
    #dCP_dThrottle = dCP/dThrottle
    
    #segment.state.conditions.aero_derivatives.dCL_dThrottle = dCL_dThrottle
    #segment.state.conditions.aero_derivatives.dCD_dThrottle = dCD_dThrottle      
    #segment.state.conditions.aero_derivatives.dCT_dThrottle = dCT_dThrottle    
    #segment.state.conditions.aero_derivatives.dCP_dThrottle = dCP_dThrottle         
    

    ## ----------------------------------------------------------------------------    
    ## Control surface deflection perturbation for each wing
    #for wing in list(segment.analyses.aerodynamics.geometry.wings.keys()):
        #if len(segment.analyses.aerodynamics.geometry.wings[wing].control_surfaces) !=0:
            ## set segment derivatives based on perturbed segment
            #for cs in list(segment.analyses.aerodynamics.geometry.wings[wing].control_surfaces.keys()):
                #delta             = segment.analyses.aerodynamics.geometry.wings[wing].control_surfaces[cs].deflection                
                #perturbed_segment = deepcopy(segment)    
                #delta_plus        = delta + 0.1
                #perturbed_segment.analyses.aerodynamics.geometry.wings[wing].control_surfaces[cs].deflection = delta_plus
                
                #iterate = perturbed_segment.process.iterate
                #iterate.conditions(perturbed_segment)                 
                
                #dDelta          = perturbed_segment.analyses.aerodynamics.geometry.wings[wing].control_surfaces[cs].deflection - segment.analyses.aerodynamics.geometry.wings[wing].control_surfaces[cs].deflection
                #dCL             = perturbed_segment.state.conditions.aerodynamics.lift_coefficient - segment.state.conditions.aerodynamics.lift_coefficient
                #dCD             = perturbed_segment.state.conditions.aerodynamics.drag_coefficient - segment.state.conditions.aerodynamics.drag_coefficient
                
                ## roll and yaw moment coefficient derivatives
                #if surrogate_used:
                    #print("Surrogate model is being used. No roll or yaw coefficients available.")
                    #dCM = 0
                    #dCn = 0
                    #dCl = 0
                #else:
                    ## use VLM outputs directly
                    #dCn = perturbed_segment.state.conditions.static_stability.yawing_moment_coefficient - segment.state.conditions.static_stability.yawing_moment_coefficient
                    #dCl = perturbed_segment.state.conditions.static_stability.rolling_moment_coefficient - segment.state.conditions.static_stability.rolling_moment_coefficient              
                    #dCM = perturbed_segment.state.conditions.aerodynamics.moment_coefficient - segment.state.conditions.aerodynamics.moment_coefficient
                    
                ## propeller derivatives 
                #dCT, dCP = propeller_derivatives(segment, perturbed_segment, n_cpts) 
                    
                #dCL_dDelta      = dCL/dDelta 
                #dCD_dDelta      = dCD/dDelta
                #dCM_dDelta      = dCM/dDelta
                #dCn_dDelta      = dCn/dDelta            
                #dCl_dDelta      = dCl/dDelta           
                #dCT_dDelta      = dCT/dDelta        
                #dCP_dDelta      = dCP/dDelta
                #dCL_dDelta_tag  = 'dCL_dDelta_'+cs
                #dCD_dDelta_tag  = 'dCD_dDelta_'+cs
                #dCM_dDelta_tag  = 'dCM_dDelta_'+cs
                #dCn_dDelta_tag  = 'dCn_dDelta_'+cs  
                #dCl_dDelta_tag  = 'dCl_dDelta_'+cs   
                #dCT_dDelta_tag  = 'dCT_dDelta_'+cs   
                #dCP_dDelta_tag  = 'dCP_dDelta_'+cs  
                #segment.state.conditions.aero_derivatives[dCL_dDelta_tag]  = dCL_dDelta
                #segment.state.conditions.aero_derivatives[dCD_dDelta_tag]  = dCD_dDelta
                #segment.state.conditions.aero_derivatives[dCM_dDelta_tag]  = dCM_dDelta
                #segment.state.conditions.aero_derivatives[dCn_dDelta_tag]  = dCn_dDelta
                #segment.state.conditions.aero_derivatives[dCl_dDelta_tag]  = dCl_dDelta
                #segment.state.conditions.aero_derivatives[dCT_dDelta_tag]  = dCT_dDelta
                #segment.state.conditions.aero_derivatives[dCP_dDelta_tag]  = dCP_dDelta

    ## ----------------------------------------------------------------------------    
    ## Velocity magnitude perturbation
    #vinf                = segment.state.conditions.frames.inertial.velocity_vector
    #vmag                = np.linalg.norm(vinf,axis=1)
    #gamma               = np.arctan2(vinf[:,2],vinf[:,0])
    
    #perturbed_segment   = deepcopy(segment)    
    #vmag_plus           = vmag*(1+h) 
    #perturbed_segment.state.conditions.frames.inertial.velocity_vector[:,0] = vmag_plus*np.cos(gamma)
    #perturbed_segment.state.conditions.frames.inertial.velocity_vector[:,2] = vmag_plus*np.sin(gamma)
        
    #iterate = perturbed_segment.process.iterate
    #iterate.conditions(perturbed_segment)
    
    ## set segment derivatives based on perturbed segment
    #dV      = perturbed_segment.state.conditions.freestream.velocity - segment.state.conditions.frames.inertial.velocity_vector
    #dCL     = perturbed_segment.state.conditions.aerodynamics.lift_coefficient - segment.state.conditions.aerodynamics.lift_coefficient
    #dCD     = perturbed_segment.state.conditions.aerodynamics.drag_coefficient - segment.state.conditions.aerodynamics.drag_coefficient
    #dCL_dV  = dCL/dV   
    #dCD_dV  = dCD/dV  

    #segment.state.conditions.aero_derivatives.dCL_dV = dCL_dV  
    #segment.state.conditions.aero_derivatives.dCD_dV = dCD_dV     
    
    return 

def propeller_derivatives(segment, perturbed_segment, n_cpts):
    props = segment.state.conditions.noise.sources.propellers
    perturbed_props = perturbed_segment.state.conditions.noise.sources.propellers
    dCT = np.zeros((len(props),n_cpts,1))
    dCP = np.zeros((len(props),n_cpts,1))
    for i in range(len(props)):
        prop_key       = list(props.keys())[i]
        prop           = props[prop_key]
        perturbed_prop = perturbed_props[prop_key]
        
        dCT[i,:,:] = perturbed_prop.thrust_coefficient - prop.thrust_coefficient
        dCP[i,:,:] = perturbed_prop.power_coefficient - prop.power_coefficient
    
    return dCT, dCP

