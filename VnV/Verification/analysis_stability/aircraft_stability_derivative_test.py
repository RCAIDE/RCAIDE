'''

The script below documents how to set up and plot the results of polar analysis of full aircraft configuration 

''' 

# ----------------------------------------------------------------------
#   Imports
# ---------------------------------------------------------------------- 
import RCAIDE
from RCAIDE.Framework.Core import Units , Data   
from RCAIDE.Library.Methods.Performance                            import aircraft_aerodynamic_analysis 
from RCAIDE.Library.Plots                                          import *   
import numpy as np
import matplotlib.pyplot  as plt
import os
import  sys

# local imports 
base_dir = os.path.dirname(os.path.abspath(__file__))

vehicles_path = os.path.abspath(
    os.path.join(base_dir, "..", "..", "Vehicles")
)

if vehicles_path not in sys.path:
    sys.path.insert(0, vehicles_path)
from Navion    import vehicle_setup, configs_setup
# ----------------------------------------------------------------------
#   Main
# ---------------------------------------------------------------------- 
def main():
    
    # Truth Values for Literature : DO NOT CHANGE
    truth_vals = Data  
    truth_vals.CY_beta      = -0.195398   
    truth_vals.CL_beta      = -0.12228 
    truth_vals.CM_alpha     = -1.1509  
    truth_vals.CN_beta      = 0.074425 
    truth_vals.CY_delta_a   = 0.03569527063665028
    truth_vals.CL_delta_a   = 0.11310186875882451 
    truth_vals.Clift_delta_e= 0.5314183549838385
    truth_vals.CN_delta_a   = -0.0012032113697747287
    truth_vals.CM_delta_e   = -1.3917717801522826
    truth_vals.CY_delta_r   = -0.1098933051060919
    truth_vals.CL_delta_r   = -0.011172677005051052
    truth_vals.CN_delta_r   = 0.05993138537068411 

    vehicle  = vehicle_setup()    
    configs  = configs_setup(vehicle) 
    analyses = analyses_setup(configs)  

 
    angle_of_attack_range                 = np.array([[2 * Units.degree]])
    Mach_number_range                     = np.ones_like(angle_of_attack_range) * 0.15 
    results                               = aircraft_aerodynamic_analysis(analyses          = analyses.base,
                                                                          angle_of_attacks  = angle_of_attack_range,
                                                                          mach_numbers      = Mach_number_range, 
                                                                          altitude          =  1000. * Units.feet ) 
 
    SSD = results.static_stability.derivatives 
    
    error = Data(  
        CY_beta        = 100*np.array((truth_vals.CY_beta      - SSD.CY_beta[0, 0]      )/truth_vals.CY_beta    ),   
        CL_beta        = 100*np.array((truth_vals.CL_beta      - SSD.CL_beta[0, 0]      )/truth_vals.CL_beta    ), 
        CM_alpha       = 100*np.array((truth_vals.CM_alpha     - SSD.CM_alpha[0, 0]     )/truth_vals.CM_alpha   ),  
        CN_beta        = 100*np.array((truth_vals.CN_beta      - SSD.CN_beta[0, 0]      )/truth_vals.CN_beta    ), 
        CY_delta_a     = 100*np.array((truth_vals.CY_delta_a   - SSD.CY_delta_a[0, 0]   )/truth_vals.CY_delta_a ),
        CL_delta_a     = 100*np.array((truth_vals.CL_delta_a   - SSD.CL_delta_a[0, 0]   )/truth_vals.CL_delta_a ),
        Clift_delta_e  = 100*np.array((truth_vals.Clift_delta_e- SSD.Clift_delta_e[0, 0])/truth_vals.Clift_delta_e),
        CN_delta_a     = 100*np.array((truth_vals.CN_delta_a   - SSD.CN_delta_a[0, 0]   )/truth_vals.CN_delta_a   ),
        CM_delta_e     = 100*np.array((truth_vals.CM_delta_e   - SSD.CM_delta_e[0, 0]   )/truth_vals.CM_delta_e   ),
        CY_delta_r     = 100*np.array((truth_vals.CY_delta_r   - SSD.CY_delta_r[0, 0]   )/truth_vals.CY_delta_r   ),
        CL_delta_r     = 100*np.array((truth_vals.CL_delta_r   - SSD.CL_delta_r[0, 0]   )/truth_vals.CL_delta_r   ),
        CN_delta_r     = 100*np.array((truth_vals.CN_delta_r   - SSD.CN_delta_r[0, 0]   )/truth_vals.CN_delta_r   ), 
         
         )
     

    print('Errors:')
    print(error)

    for k,v in list(error.items()):
        print(v)
        #assert(np.abs(v)<1e-2)    
    
    return 


# ----------------------------------------------------------------------
#   Define the Vehicle Analyses
# ----------------------------------------------------------------------

def analyses_setup(configs):

    analyses = RCAIDE.Framework.Analyses.Analysis.Container()

    # build a base analysis for each config
    for tag,config in list(configs.items()):
        analysis = base_analysis(config)
        analyses[tag] = analysis
 
    return analyses


def base_analysis(vehicle):

    # ------------------------------------------------------------------
    #   Initialize the Analyses
    # ------------------------------------------------------------------     
    analyses = RCAIDE.Framework.Analyses.Vehicle() 
    analyses.vehicle =  vehicle
     
    geometry = RCAIDE.Framework.Analyses.Geometry.Geometry() 
    analyses.append(geometry)
  
    aerodynamics   = RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method()
    aerodynamics.settings.use_surrogate = False 
    analyses.append(aerodynamics)
    
    return analyses 


     
if __name__ == '__main__': 
    main()    
    plt.show()