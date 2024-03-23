## @ingroup Library-Methods-Mission-Common-Update
# RCAIDE/Library/Methods/Missions/Common/Update/stability.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Stability
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Mission-Common-Update
def stability(segment): 
    """ Updates the stability of the aircraft 
        
        Assumptions:
        N/A
        
        Inputs:
            None 
                 
        Outputs: 
            None
      
        Properties Used:
        N/A
                    
    """   
    # unpack
    conditions = segment.state.conditions
    stability_model = segment.analyses.stability
    
    # call aerodynamics model
    if stability_model:
        results = stability_model( segment.state.conditions )
        conditions.stability.update(results)
    
    return


def _stability(State, Settings, System):
	'''
	Framework version of stability.
	Wraps stability with State, Settings, System pack/unpack.
	Please see stability documentation for more details.
	'''

	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = stability('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System