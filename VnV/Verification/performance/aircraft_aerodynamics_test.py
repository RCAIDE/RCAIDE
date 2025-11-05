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
sys.path.append(os.path.join( os.path.split(os.path.split(sys.path[0])[0])[0], 'Vehicles'))
from Boeing_737    import vehicle_setup as b737_vehicle_setup 
from BWB    import vehicle_setup  as   bwb_vehicle_setup
# ----------------------------------------------------------------------
#   Main
# ---------------------------------------------------------------------- 
def main(): 
    Boeing_737_Drag_Polar()
    BWB_Drag_Polar()

    return 

def Boeing_737_Drag_Polar():

    vehicle                               = b737_vehicle_setup()   
    angle_of_attack_range                 = np.atleast_2d(np.linspace(-5, 25, 18)).T*Units.degrees   
    Mach_number_range                     = np.ones_like(angle_of_attack_range) * 0.78
    aerodynamics_analysis_routine         = RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method()
    aerodynamics_analysis_routine.vehicle = vehicle
    temperatures                          = np.ones_like(angle_of_attack_range) * 340
    non_dimensional_reynolds_numbers      = np.ones_like(angle_of_attack_range) * 1E7
    results                               = aircraft_aerodynamic_analysis(aerodynamics_analysis = aerodynamics_analysis_routine,
                                                                          angle_of_attacks = angle_of_attack_range,
                                                                      non_dimensional_reynolds_numbers = non_dimensional_reynolds_numbers,
                                                                      temperatures                     = temperatures,
                                                                      mach_numbers = Mach_number_range)

    results                           = aircraft_aerodynamic_analysis(aerodynamics_analysis = aerodynamics_analysis_routine,
                                                                      angle_of_attacks = angle_of_attack_range,
                                                                      mach_numbers = Mach_number_range,
                                                                      altitude  = 0)

    CL_truth = np.array([-0.38186938, -0.10627372,  0.16950056,  0.4455403 ,  0.72072764,
                         0.99313006,  1.26355613,  1.5300295 ,  1.78970029,  2.04543276,
                         2.24649627,  2.35313159,  2.4597669 ,  2.56640222,  2.67303754,
                         2.77967285,  2.88630817,  2.99294349])
    
    CD_truth = np.array([0.06682168, 0.03297028, 0.02150798, 0.02273792, 0.04049766,
                         0.07110456, 0.09480261, 0.10963991, 0.15831249, 0.24051187,
                         0.36893079, 0.56138268, 0.84474023, 1.24610486, 1.79621305,
                         2.5294356 , 3.48377719, 4.70087622])
                      
    # plot results 
    plot_aircraft_aerodynamics(results, save_filename = "B737_Aircraft_Aerodynamic_Analysis")    
    
    # check errors 
    CL_error = np.max(np.abs(results.lift_coefficient[:, 0]-CL_truth))
    assert(CL_error<1e-6)

    CD_truth = np.max(np.abs(results.drag_coefficient[:, 0]-CD_truth))    
    assert(CL_error<1e-6)
      
    
    return  



def BWB_Drag_Polar():

    vehicle                               = bwb_vehicle_setup()   
    angle_of_attack_range                 = np.atleast_2d(np.linspace(-5, 25, 18)).T*Units.degrees   
    Mach_number_range                     = np.ones_like(angle_of_attack_range) * 0.78
    aerodynamics_analysis_routine         = RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method()
    aerodynamics_analysis_routine.vehicle = vehicle
    temperatures                          = np.ones_like(angle_of_attack_range) * 340
    non_dimensional_reynolds_numbers      = np.ones_like(angle_of_attack_range) * 1E7
    results                               = aircraft_aerodynamic_analysis(aerodynamics_analysis = aerodynamics_analysis_routine,
                                                                          angle_of_attacks = angle_of_attack_range,
                                                                      non_dimensional_reynolds_numbers = non_dimensional_reynolds_numbers,
                                                                      temperatures                     = temperatures,
                                                                      mach_numbers = Mach_number_range)

    results                           = aircraft_aerodynamic_analysis(aerodynamics_analysis = aerodynamics_analysis_routine,
                                                                      angle_of_attacks = angle_of_attack_range,
                                                                      mach_numbers = Mach_number_range,
                                                                      altitude  = 0)

    CL_truth = np.array([-0.56059439, -0.32542092, -0.08989688,  0.14640192,  0.38242356,
                    0.61668368,  0.84951268,  1.07947942,  1.30422185,  1.52593968,
                    1.70276748,  1.80205797,  1.90134846,  2.00063894,  2.09992943,
                    2.19921992,  2.29851041,  2.3978009 ])

    CD_truth = np.array([0.03404038, 0.03083873, 0.01588543, 0.01248107, 0.01749438,
                        0.02983582, 0.07156736, 0.11865501, 0.1906569 , 0.25303808,
                        0.26509919, 0.27679681, 0.28853782, 0.30032217, 0.31214983,
                        0.32402081, 0.33593508, 0.34789266])

    plot_aircraft_aerodynamics(results,  save_filename = "BWB_Aircraft_Aerodynamic_Analysis")


    CL_error = np.max(np.abs(results.lift_coefficient[:, 0]-CL_truth))
    assert(CL_error<1e-6)

    CD_truth = np.max(np.abs(results.drag_coefficient[:, 0]-CD_truth))    
    assert(CL_error<1e-6)
    
    return 
     
if __name__ == '__main__': 
    main()    
    plt.show()