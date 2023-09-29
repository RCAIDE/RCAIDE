## @ingroup Methods-Thermal_Management-Batteries-Sizing
# size_battery_thermal_management_system.py
#  
# Modified: Jun 2023, M. Clarke   
import MARC.Methods.Thermal_Management.Batteries.Sizing.btms_sizing_setup             as btms_sizing_setup 
import MARC.Methods.Thermal_Management.Batteries.Sizing.set_optimized_btms_paramters  as set_optimized_btms_paramters   

import MARC.Optimization.Package_Setups.scipy_setup                    as scipy_setup      
import numpy as np  
import time

# ----------------------------------------------------------------------
#  Methods
# ----------------------------------------------------------------------
## @ingroup Methods-Thermal_Management-Batteries-Sizing
def size_battery_thermal_management_system(battery, single_side_contact=True, dry_mass=True,solver_name= 'SLSQP',iterations = 200,
                      solver_sense_step = 1E-4,solver_tolerance = 1E-3,print_iterations = False):

    """  

    """
    
    # initiate time for sizing optimization 
    ti                   = time.time()   
    
    # unpack btms model from battery
    btms                 = battery.thermal_management_system 
      
    # set up optimiztion problem 
    optimization_problem = btms_sizing_setup(battery,print_iterations)
    
    # run optimization problem
    output               = scipy_setup.SciPy_Solve(optimization_problem,solver=solver_name, iter = iterations , sense_step = solver_sense_step,tolerance = solver_tolerance)  

    # print optimization results 
    print (output)    
    
    # set remaining btms variables using optimized parameters         
    btms                 = set_optimized_btms_paramters(btms,optimization_problem)  
        
    # end wall clock time of sizing optimization 
    tf                   = time.time()
    elapsed_time         = round((tf-ti)/60,2)
    print('BTMS Optimization Simulation Time: ' + str(elapsed_time) + ' mins')    
 
    return battery