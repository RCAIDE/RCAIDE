## @ingroup methods-mission-segments
# expand_state.py
# 
# Created:  Jul 2014, SUAVE Team
# Modified: Jan 2016, E. Botero

# ----------------------------------------------------------------------
#  Expand State
# ----------------------------------------------------------------------

## @ingroup methods-mission-segments
def func_expand_state(segment):
    
    """Makes all vectors in the state the same size.

    Assumptions:
    N/A

    Source:
    N/A

    Inputs:
    state.numerics.number_control_points  [Unitless]

    Outputs:
    N/A

    Properties Used:
    N/A
    """       

    n_points = segment.state.numerics.number_control_points
    
    segment.state.expand_rows(n_points)
    
    return
    


def expand_state(State, Settings, System):
	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = func_expand_state('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System