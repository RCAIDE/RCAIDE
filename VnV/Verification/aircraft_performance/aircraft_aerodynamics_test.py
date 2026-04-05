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
from Boeing_737    import vehicle_setup   as B737_vehicle_setup  
from Boeing_737    import configs_setup   as B737_configs_setup 
from BWB           import vehicle_setup   as BWB_vehicle_setup
from BWB           import configs_setup   as BWB_configs_setup 
# ----------------------------------------------------------------------
#   Main
# ---------------------------------------------------------------------- 
def main(): 
    Boeing_737_Drag_Polar()
    BWB_Drag_Polar()

    return 

def Boeing_737_Drag_Polar():

    vehicle  = B737_vehicle_setup()    
    configs  = B737_configs_setup(vehicle) 
    analyses = analyses_setup(configs)  
    
    angle_of_attack_range                 = np.atleast_2d(np.linspace(-5, 25, 18)).T*Units.degrees   
    Mach_number_range                     = np.ones_like(angle_of_attack_range) * 0.78 
    temperatures                          = np.ones_like(angle_of_attack_range) * 340
    non_dimensional_reynolds_numbers      = np.ones_like(angle_of_attack_range) * 1E7
    results                               = aircraft_aerodynamic_analysis(analyses                         = analyses.base,
                                                                          angle_of_attacks                 = angle_of_attack_range,
                                                                          non_dimensional_reynolds_numbers = non_dimensional_reynolds_numbers,
                                                                          temperatures                     = temperatures,
                                                                          mach_numbers                     = Mach_number_range)

    results                           = aircraft_aerodynamic_analysis(analyses                         = analyses.base,
                                                                      angle_of_attacks                 = angle_of_attack_range,
                                                                      mach_numbers = Mach_number_range,
                                                                      altitude  = 0)

    CL_truth = np.array([-0.36969888, -0.10394546,  0.16198486,  0.42818621,  0.69358781,
                         0.95634793,  1.21722618,  1.47434069,  1.72496022,  1.97181948,
                         2.16606678,  2.26943886,  2.37281094,  2.47618303,  2.57955511,
                         2.68292719,  2.78629927,  2.88967136])
    CD_truth = np.array([0.0313375 , 0.03055797, 0.02153682, 0.02028306, 0.02940625,
                         0.05473865, 0.08165471, 0.10323526, 0.15642946, 0.21429303,
                         0.2256376 , 0.23404399, 0.2425397 , 0.25112333, 0.25979418,
                         0.2685519 , 0.27739632, 0.28632736])
                      
    # plot results 
    plot_aircraft_aerodynamics(results, save_filename = "B737_Aircraft_Aerodynamic_Analysis")    
    
    # check errors 
    CL_error = np.max(np.abs(results.lift_coefficient[:, 0]-CL_truth))
    assert(CL_error<1e-6)

    CD_truth = np.max(np.abs(results.drag_coefficient[:, 0]-CD_truth))    
    assert(CL_error<1e-6)
      
    
    return   

def BWB_Drag_Polar():

    vehicle  = BWB_vehicle_setup()    
    configs  = BWB_configs_setup(vehicle) 
    analyses = analyses_setup(configs)
    
    angle_of_attack_range                 = np.atleast_2d(np.linspace(-5, 25, 18)).T*Units.degrees   
    Mach_number_range                     = np.ones_like(angle_of_attack_range) * 0.78 
    temperatures                          = np.ones_like(angle_of_attack_range) * 340
    non_dimensional_reynolds_numbers      = np.ones_like(angle_of_attack_range) * 1E7
    results                               = aircraft_aerodynamic_analysis(analyses                         = analyses.cruise,
                                                                          angle_of_attacks                 = angle_of_attack_range,
                                                                          non_dimensional_reynolds_numbers = non_dimensional_reynolds_numbers,
                                                                          temperatures                     = temperatures,
                                                                          mach_numbers                     = Mach_number_range)

    results                           = aircraft_aerodynamic_analysis(analyses         = analyses.cruise,
                                                                      angle_of_attacks = angle_of_attack_range,
                                                                      mach_numbers     = Mach_number_range,
                                                                      altitude         = 0)

    CL_truth = np.array([-0.8859043 , -0.57402438, -0.26155033,  0.05231007,  0.36610444,
                        0.67798436,  0.98814569,  1.29486985,  1.59508185,  1.89152364,
                        2.12963852,  2.26700691,  2.4043753 ,  2.54174368,  2.67911207,
                        2.81648046,  2.95384884,  3.09121723])

    CD_truth = np.array([0.04902018, 0.0432557 , 0.02050936, 0.01461097, 0.02046714,
                        0.03695656, 0.08905799, 0.14631973, 0.22536315, 0.32287296,
                        0.33891408, 0.35478732, 0.37077092, 0.38686488, 0.40306919,
                        0.41938387, 0.43580891, 0.45234431])

    plot_aircraft_aerodynamics(results,  save_filename = "BWB_Aircraft_Aerodynamic_Analysis")


    CL_error = np.max(np.abs(results.lift_coefficient[:, 0]-CL_truth))
    assert(CL_error<1e-6)

    CD_truth = np.max(np.abs(results.drag_coefficient[:, 0]-CD_truth))    
    assert(CL_error<1e-6)
    
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
    analyses.append(aerodynamics)
    
    return analyses 


     
if __name__ == '__main__': 
    main()    
    plt.show()