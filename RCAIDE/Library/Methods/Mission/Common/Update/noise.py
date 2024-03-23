## @ingroup Library-Methods-Mission-Segments-Common-Update
# RCAIDE/Library/Methods/Missions/Common/Update/noise.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  compute_noise
# ----------------------------------------------------------------------------------------------------------------------

## @ingroup Library-Methods-Mission-Segments-Common-Update
def noise(segment):
    """ Updates the noise produced by the vehicle
        
        Assumptions:
        N/A
        
        Inputs:
            None 
                 
        Outputs: 
            None
      
        Properties Used:
        N/A
                    
    """   
    noise_model = segment.analyses.noise
    
    if noise_model:
        noise_model.evaluate_noise(segment)    


def _noise(State, Settings, System):
	'''
	Framework version of noise.
	Wraps noise with State, Settings, System pack/unpack.
	Please see noise documentation for more details.
	'''

	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = noise('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System