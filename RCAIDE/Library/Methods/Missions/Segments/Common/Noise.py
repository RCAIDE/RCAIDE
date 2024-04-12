## @ingroup Methods-Missions-Segments-Common
# Noise.py
# 
# Created:  Oct 2020, M. Clarke

# ----------------------------------------------------------------------
#  Update Noise
# ----------------------------------------------------------------------
## @ingroup Methods-Missions-Segments-Common
def func_compute_noise(segment):
    """ Evaluates the energy network to find the thrust force and mass rate

        Inputs -
            segment.analyses.noise             [Function]

        Outputs
            N/A

        Assumptions -


    """    
    noise_model = segment.analyses.noise
    
    if noise_model:
        noise_model.evaluate_noise(segment)    


compute_noise(State, Settings, System):
	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = func_compute_noise('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System