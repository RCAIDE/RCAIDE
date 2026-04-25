# RCAIDE/Library/Methods/Aerodynamics/Vortex_Lattice_Method/train_AVL_surrogates.py
#  
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
import RCAIDE 
from RCAIDE.Framework.Mission.Common                                             import Results  
from RCAIDE.Library.Methods.Aerodynamics.Athena_Vortex_Lattice.run_AVL_analysis  import run_AVL_analysis  
 
# Package imports 
import os
import numpy as np
from shutil import rmtree    

# ----------------------------------------------------------------------------------------------------------------------
#  train_AVL_surrogates
# ---------------------------------------------------------------------------------------------------------------------- 
def train_AVL_surrogates(aerodynamics,vehicle):
    """Call methods to run VLM for sample point evaluation. 
    
    Assumptions:
        None
        
    Source:
        None

    Args:
        aerodynamics       : VLM analysis          [unitless] 
        
    Returns: 
        None    
    """ 
 
    run_folder             = os.path.abspath(aerodynamics.settings.filenames.run_folder) 
    training               = aerodynamics.training  
    AoA                    = training.angle_of_attack
    Mach                   = training.Mach
    side_slip_angle        = aerodynamics.settings.side_slip_angle
    roll_rate_coefficient  = aerodynamics.settings.roll_rate_coefficient
    pitch_rate_coefficient = aerodynamics.settings.pitch_rate_coefficient
    lift_coefficient       = aerodynamics.settings.lift_coefficient
    n_sw                   = aerodynamics.settings.number_of_spanwise_vortices 
    atmosphere             = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    atmo_data              = atmosphere.compute_values(altitude = 0.0)         
    
    n_wings = 0  
    for wing in vehicle.wings:         
        n_wings += 1 
        if wing.xz_plane_symmetric: 
            n_wings += 1
            
    len_AoA  = len(AoA)
    len_Mach = len(Mach)
    training.CL_y     = np.zeros((len_AoA,len_Mach,n_sw*n_wings))
    training.CL       = np.zeros((len_AoA,len_Mach))
    training.CDi      = np.zeros((len_AoA,len_Mach))
    training.CM       = np.zeros((len_AoA,len_Mach))
    training.e        = np.zeros((len_AoA,len_Mach))
    training.Cm_alpha = np.zeros((len_AoA,len_Mach))
    training.Cn_beta  = np.zeros((len_AoA,len_Mach))
    training.NP       = np.zeros((len_AoA,len_Mach))

    # remove old files in run directory  
    if os.path.exists(aerodynamics.settings.filenames.run_folder):
        if aerodynamics.settings.new_regression_results:
            rmtree(run_folder)

    for i,_ in enumerate(Mach):
        # Set training conditions
        run_conditions = Results()
        run_conditions.expand_rows(len_AoA)
        run_conditions.aerodynamics.angles.alpha           = np.array([AoA]).T  
        run_conditions.freestream.density                  = np.ones_like(run_conditions.aerodynamics.angles.alpha)*atmo_data.density 
        run_conditions.freestream.gravity                  = np.ones_like(run_conditions.aerodynamics.angles.alpha)*9.81          
        run_conditions.freestream.speed_of_sound           = np.ones_like(run_conditions.aerodynamics.angles.alpha)*atmo_data.speed_of_sound[0,0]  
        run_conditions.freestream.velocity                 = np.ones_like(run_conditions.aerodynamics.angles.alpha)*Mach[i] * run_conditions.freestream.speed_of_sound 
        run_conditions.freestream.mach_number              = np.ones_like(run_conditions.aerodynamics.angles.alpha)*Mach[i]
        run_conditions.aerodynamics.angles.beta            = np.ones_like(run_conditions.aerodynamics.angles.alpha)*side_slip_angle 
        run_conditions.static_stability.coefficients.roll  = np.ones_like(run_conditions.aerodynamics.angles.alpha)*roll_rate_coefficient   
        if lift_coefficient == None: 
            run_conditions.aerodynamics.coefficients.lift.inviscid.total= lift_coefficient
        else:
            run_conditions.aerodynamics.coefficients.lift.inviscid.total= np.array([lift_coefficient]).T  
        run_conditions.static_stability.coefficients.pitch = np.ones_like(run_conditions.aerodynamics.angles.alpha)*pitch_rate_coefficient 

        # Run Analysis at AoA[i] and Mach[i]
        run_AVL_analysis(aerodynamics,run_conditions, vehicle) 
 
        Clift_y_res  = run_conditions.aerodynamics.coefficients.lift.spanwise 
        Clift_res    = run_conditions.aerodynamics.coefficients.lift.inviscid.total 
        Cdrag_res    = run_conditions.aerodynamics.coefficients.drag.induced.total    
        e_res        = run_conditions.aerodynamics.coefficients.drag.induced.efficiency_factor 
        CM_res       = run_conditions.static_stability.coefficients.pitch 
        Cm_alpha_res = run_conditions.static_stability.derivatives.CM_alpha 
        Cn_beta_res  = run_conditions.static_stability.derivatives.CN_beta 
        NP_res       = run_conditions.static_stability.neutral_point  
         
        training.CL_y[:,i]       =  Clift_y_res 
        training.CL[:,i]         =  Clift_res[:,0]   
        training.CDi[:,i]        =  Cdrag_res[:,0]   
        training.CM[:,i]         =  CM_res[:,0]    
        training.e[:,i]          =  e_res[:,0]         
        training.Cm_alpha[:,i]   =  Cm_alpha_res[:,0]
        training.Cn_beta[:,i]    =  Cn_beta_res[:,0] 
        training.NP[:,i]         =  NP_res[:,0]   
 
    return training