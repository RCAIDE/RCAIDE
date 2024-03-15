## @ingroup Library-Methods-Noise-Common 
# RCAIDE/Library/Methods/Noise/Common/background_noise.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke  
 
# ----------------------------------------------------------------------------------------------------------------------  
#  Bakcground Noise 
# ----------------------------------------------------------------------------------------------------------------------      
## @ingroup Library-Methods-Noise-Common
def background_noise():
    '''
    This is sound pressure level of background noise  
    
    Assumptions:
       N/A

    Source:
        None
        
    Inputs:
        None

    Outputs: 
        None
        
    Properties Used:
        None 
    
    '''
    return 32


def _background_noise(State, Settings, System):
	'''
	Framework version of background_noise.
	Wraps background_noise with State, Settings, System pack/unpack.
	Please see background_noise documentation for more details.
	'''


	results = background_noise()
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System