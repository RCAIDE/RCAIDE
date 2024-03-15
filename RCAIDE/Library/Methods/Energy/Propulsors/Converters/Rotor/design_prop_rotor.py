## @ingroup Methods-Energy-Propulsors
# RCAIDE/Library/Methods/Energy/Propulsors/design_prop_rotor.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  

# RCAIDE Imports    
from RCAIDE.Framework.Optimization.Packages.scipy                                     import scipy_setup
from RCAIDE.Library.Methods.Energy.Propulsors.Converters.Rotor.Design.optimization_setup       import optimization_setup
from RCAIDE.Library.Methods.Energy.Propulsors.Converters.Rotor.Design.set_optimized_parameters import set_optimized_parameters

# Python package imports   
import time 

# ----------------------------------------------------------------------------------------------------------------------  
#  Design Prop-rotor
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Methods-Energy-Propulsors
def design_prop_rotor(rotor,number_of_stations = 20,solver_name= 'SLSQP',iterations = 200,
                      solver_sense_step = 1E-4,solver_tolerance = 1E-3,print_iterations = False):  
    """ Optimizes prop-rotor chord and twist given input parameters to meet either design power or thurst. 
        This scrip adopts RCAIDE's native optimization style where the objective function is expressed 
        as an aeroacoustic function, considering both efficiency and radiated noise.
          
          Inputs: 
          prop_attributes.
              hub radius                       [m]
              tip radius                       [m]
              rotation rate                    [rad/s]
              freestream velocity              [m/s]
              number of blades                 [None]       
              number of stations               [None]
              design lift coefficient          [None]
              airfoil data                     [None]
              optimization_parameters.
                 slack_constaint               [None]
                 ideal_SPL_dbA                 [dBA]
                 multiobjective_aeroacoustic_weight           [None]
            
          Outputs:
          Twist distribution                   [array of radians]
          Chord distribution                   [array of meters]
              
          Assumptions: 
             N/A 
        
          Source:
             None 
    """    

    # Unpack rotor geometry  
    rotor_tag     = rotor.tag
    rotor.tag     = 'rotor'
    
    # start optimization 
    ti                   = time.time()   
    optimization_problem = optimization_setup(rotor,number_of_stations,print_iterations)
    output               = scipy_setup.SciPy_Solve(optimization_problem,solver=solver_name, iter = iterations , sense_step = solver_sense_step,tolerance = solver_tolerance)    
    tf                   = time.time()
    elapsed_time         = round((tf-ti)/60,2)
    print('Lift-rotor Optimization Simulation Time: ' + str(elapsed_time) + ' mins')   
    
    # print optimization results 
    print (output)  
    
    # set remaining rotor variables using optimized parameters 
    rotor     = set_optimized_parameters(rotor,optimization_problem)
    rotor.tag = rotor_tag
     
    return rotor
   


def _design_prop_rotor(State, Settings, System):
	'''
	Framework version of design_prop_rotor.
	Wraps design_prop_rotor with State, Settings, System pack/unpack.
	Please see design_prop_rotor documentation for more details.
	'''

	#TODO: rotor              = [Replace With State, Settings, or System Attribute]
	#TODO: number_of_stations = [Replace With State, Settings, or System Attribute]
	#TODO: solver_name        = [Replace With State, Settings, or System Attribute]
	#TODO: iterations         = [Replace With State, Settings, or System Attribute]
	#TODO: solver_sense_step  = [Replace With State, Settings, or System Attribute]
	#TODO: solver_tolerance   = [Replace With State, Settings, or System Attribute]
	#TODO: print_iterations   = [Replace With State, Settings, or System Attribute]

	results = design_prop_rotor('rotor', 'number_of_stations', 'solver_name', 'iterations', 'solver_sense_step', 'solver_tolerance', 'print_iterations')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System