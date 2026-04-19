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
    
    # Truth Values for Literature RANGE
    truth_vals = Data()  
    truth_vals.Clift_alpha  = np.array([4.2,5.5])
    truth_vals.CY_beta      = np.array([-0.77, -0.2])
    truth_vals.CL_beta      = np.array([-0.1, -0.05])
    truth_vals.CM_alpha     = np.array([-1.24,-0.5])
    truth_vals.CN_beta      = np.array([0.033,0.09])
    truth_vals.CL_p         = np.array([-0.48, -0.3])
    truth_vals.CL_r         = np.array([0.07,0.27])
    truth_vals.CM_q         = np.array([-13.29,-9.5])
    truth_vals.CN_p         = np.array([-0.1, -0.01])
    truth_vals.CN_r         = np.array([-0.14, -0.06]) 
    truth_vals.CM_delta_e   = np.array([-1.5, -1.42]) 
    truth_vals.CL_delta_a   = np.array([-0.152, -0.135 ]) 
    truth_vals.CN_delta_a   = np.array([ -0.0047, -0.0013]) 
    truth_vals.CN_delta_r   = np.array([-0.093, -0.075 ])

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
    
    
    

    print('Literature Validation ')
    for key ,val in list(truth_vals.items()):
        violation = truth_vals[key][0] < SSD[key][0, 0] and    truth_vals[key][1] > SSD[key][0, 0]
        
        lower_bound_violation_percent_error = 100* abs((truth_vals[key][0] - SSD[key][0, 0]) / truth_vals[key][0])
        upper_bound_violation_percent_error = 100* abs((truth_vals[key][1] - SSD[key][0, 0]) / truth_vals[key][1])
        
        max_percent_error = np.maximum(lower_bound_violation_percent_error, upper_bound_violation_percent_error)
        
        #print(SSD[key][0, 0])
        if not violation:
            if  truth_vals[key][1] > SSD[key][0, 0]:
                max_percent_error =  lower_bound_violation_percent_error
            if truth_vals[key][0] < SSD[key][0, 0]:
                max_percent_error =  upper_bound_violation_percent_error
                
            print(key,round(SSD[key][0, 0],5) , ' outside range by ',  round(max_percent_error,2), ' % error')
        else:
            print(key,round(SSD[key][0, 0],5) , ' inside range')
            pass
        
        
    print('Code Verification ') 
    RCAIDE_vals =  Data(
        Clift_alpha  =  5.663182777339578,
        CY_beta      =  -0.18174387734491426,
        CL_beta      =  -0.06441348396456854,
        CM_alpha     =  -0.5907098084561294,
        CN_beta      =  0.10421770287799646,
        CL_p         =  -0.4349816015743195,
        CL_r         =  0.07611568482101333,
        CM_q         =  -11.892129367279713,
        CN_p         =  0.08505107940383129,
        CN_r         =  -0.08566221462750548,
        CM_delta_e   =  -1.4287545138251625,
        CL_delta_a   =  -0.11989294569163032,
        CN_delta_a   =  -0.009873956481831609,
        CN_delta_r   =  -0.026516714863727444,
        )
          

    RCAIDE_error = Data()
    for key ,val in list(RCAIDE_vals.items()):
        RCAIDE_error[key] = abs((RCAIDE_vals[key] - SSD[key][0, 0]) / RCAIDE_vals[key])     
    
   
    print('Errors:')
    print(RCAIDE_error)

    for k,v in list(RCAIDE_error.items()):
        print(v)
        assert(np.abs(v)<1e-6)
         
    
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
    aerodynamics.settings.number_of_spanwise_vortices    = 20
    aerodynamics.settings.number_of_chordwise_vortices   = 5
    analyses.append(aerodynamics)
    
    return analyses 


     
if __name__ == '__main__': 
    main()    
    plt.show()