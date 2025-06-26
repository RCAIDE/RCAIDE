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
from RCAIDE.Library.Methods.Geometry.Planform.wing_planform import wing_planform

# local imports 
sys.path.append(os.path.join( os.path.split(os.path.split(sys.path[0])[0])[0], 'Vehicles'))
from Boeing_737    import vehicle_setup as vehicle_setup 
# ----------------------------------------------------------------------
#   Main
# ---------------------------------------------------------------------- 
def main(): 

    vehicle                           = vehicle_setup()  
    for wing in vehicle.wings: 
        wing_planform(wing,overwrite_reference =  True) 
        if isinstance(wing, RCAIDE.Library.Components.Wings.Main_Wing):
            vehicle.reference_area = wing.areas.reference
    Mach_number_range                 = np.atleast_2d(np.linspace(0.1, 0.9, 10)).T
    angle_of_attack_range             = np.atleast_2d(np.linspace(-5, 12, 18)).T*Units.degrees  
    
    aerodynamics_analysis_routine     = RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method()
    aerodynamics_analysis_routine.vehicle = vehicle
    
    results                           = aircraft_aerodynamic_analysis(aerodynamics_analysis = aerodynamics_analysis_routine,
                                                                      angle_of_attacks = angle_of_attack_range,
                                                                      mach_numbers = Mach_number_range)
  
    plot_aircraft_aerodynamics(results) 
    
    return  
  
if __name__ == '__main__': 
    main()    
    plt.show()