## @ingroup Library-Methods-Mission-Segments
# RCAIDE/Library/Methods/Missions/Segments/converge_root.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# Package imports 
import scipy.optimize
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
# converge root
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Mission-Segments
def converge_root(segment):
    """Interfaces the mission to a numerical solver. The solver may be changed by using root_finder.

    Assumptions:
    N/A

    Source:
    N/A

    Inputs:
    segment                            [Data]
    segment.settings.root_finder       [Data]
    state.numerics.tolerance_solution  [Unitless]

    Outputs:
    state.unknowns                     [Any]
    segment.state.numerics.converged   [Unitless]

    Properties Used:
    N/A
    """       
    
    unknowns = segment.state.unknowns.pack_array()
    
    try:
        root_finder = segment.settings.root_finder
    except AttributeError:
        root_finder = scipy.optimize.fsolve 
    
    unknowns,infodict,ier,msg = root_finder( iterate,
                                         unknowns,
                                         args = segment,
                                         xtol = segment.state.numerics.tolerance_solution,
                                         maxfev = segment.state.numerics.max_evaluations,
                                         epsfcn = segment.state.numerics.step_size,
                                         full_output = 1)
    
    if ier!=1:
        print("Segment did not converge. Segment Tag: " + segment.tag)
        print("Error Message:\n" + msg)
        segment.state.numerics.converged = False
        segment.converged = False
    else:
        segment.state.numerics.converged = True
        segment.converged = True
                            
    return
    
# ---------------------------------------------------------------------------------------------------------------------- 
#  Helper Functions
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Mission-Segments
def iterate(unknowns, segment):
    
    """Runs one iteration of of all analyses for the mission.

    Assumptions:
    N/A

    Source:
    N/A

    Inputs:
    state.unknowns                [Data]
    segment.process.iterate       [Data]

    Outputs:
    residuals                     [Unitless]

    Properties Used:
    N/A
    """       
    if isinstance(unknowns,np.ndarray):
        segment.state.unknowns.unpack_array(unknowns)
    else:
        segment.state.unknowns = unknowns
        
    segment.process.iterate(segment)
    
    residuals = segment.state.residuals.pack_array()
        
    return residuals 


def _converge_root(State, Settings, System):
	'''
	Framework version of converge_root.
	Wraps converge_root with State, Settings, System pack/unpack.
	Please see converge_root documentation for more details.
	'''

	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = converge_root('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System


def _iterate(State, Settings, System):
	'''
	Framework version of iterate.
	Wraps iterate with State, Settings, System pack/unpack.
	Please see iterate documentation for more details.
	'''

	#TODO: unknowns = [Replace With State, Settings, or System Attribute]
	#TODO: segment  = [Replace With State, Settings, or System Attribute]

	results = iterate('unknowns', 'segment')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System