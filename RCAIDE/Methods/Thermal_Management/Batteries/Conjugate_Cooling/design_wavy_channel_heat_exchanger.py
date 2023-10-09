## @ingroup Methods-Thermal_Management-Batteries
# design_wavy_channel_heat_exchanger.py  

# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------   
from RCAIDE.Methods.Thermal_Management.Batteries.Conjugate_Cooling.Wavy_Channel_Heat_Exchanger_Design.optimization_setup       import optimization_setup
from RCAIDE.Methods.Thermal_Management.Batteries.Conjugate_Cooling.Wavy_Channel_Heat_Exchanger_Design.set_optimized_parameters import set_optimized_parameters

# Python package imports  
from numpy import linalg as LA  
import numpy as np 
import scipy as sp 
import time 

# ----------------------------------------------------------------------
#  Rotor Design
# ----------------------------------------------------------------------
## @ingroup Methods-Thermal_Management-Batteries
def design_wavy_channel_heat_exchanger(btms, battery, single_side_contact=True, dry_mass=True,
                                       solver_name= 'SLSQP',iterations = 200,solver_sense_step = 1E-5,
                                       solver_tolerance = 1E-6,print_iterations = False):  
    """ 
    """    
    # Unpack rotor geometry   
    
    # start optimization 
    ti                   = time.time()   
    optimization_problem = optimization_setup(btms, battery, single_side_contact,dry_mass,print_iterations)
    output               = scipy_setup.SciPy_Solve(optimization_problem,solver=solver_name, iter = iterations , sense_step = solver_sense_step,tolerance = solver_tolerance)  
    
    tf                   = time.time()
    elapsed_time         = round((tf-ti)/60,2)
    print('Channel Cooling BTMS Optimization Simulation Time: ' + str(elapsed_time) + ' mins')   
    
    # print optimization results 
    print (output)  
    
    # set remaining rotor variables using optimized parameters 
    btms     = set_optimized_parameters(btms,optimization_problem) 
    
    return btms