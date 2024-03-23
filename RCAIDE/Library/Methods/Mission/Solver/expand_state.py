## @ingroup Library-Methods-Mission-Segments 
# RCAIDE/Library/Methods/Missions/Segments/expand_state.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke   

# ----------------------------------------------------------------------------------------------------------------------
# Expand State
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Mission-Segments 
def expand_state(segment):
    
    """Makes all vectors in the state the same size.

    Assumptions:
    N/A

    Source:
    N/A

    Inputs:
    state.numerics.number_of_control_points  [Unitless]

    Outputs:
    N/A

    Properties Used:
    N/A
    """       

    n_points = segment.state.numerics.number_of_control_points
    
    segment.state.expand_rows(n_points)
    
    return
    


def _expand_state(State, Settings, System):
	'''
	Framework version of expand_state.
	Wraps expand_state with State, Settings, System pack/unpack.
	Please see expand_state documentation for more details.
	'''

	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = expand_state('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System