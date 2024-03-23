## @ingroup Library-Methods-Mission-Common-Update 
# RCAIDE/Library/Methods/Missions/Common/Update/acceleration.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# Update Acceleration
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Mission-Common-Update  
def acceleration(segment):
    """ Differentiates the velocity vector to get accelerations
    
        Assumptions:
        Assumes a flat earth, this is planar motion.
        
        Inputs:
            segment.state.conditions:
                frames.inertial.velocity_vector     [meters/second]
            segment.state.numerics.time.differentiate       [float]
            
        Outputs:
            segment.state.conditions:           
                frames.inertial.acceleration_vector [meters]

        Properties Used:
        N/A
                                
    """            
    
    # unpack conditions
    v = segment.state.conditions.frames.inertial.velocity_vector
    D = segment.state.numerics.time.differentiate
    
    # accelerations
    acc = np.dot(D,v)
    
    # pack conditions
    segment.state.conditions.frames.inertial.acceleration_vector[:,:] = acc[:,:]   


def _acceleration(State, Settings, System):
	'''
	Framework version of acceleration.
	Wraps acceleration with State, Settings, System pack/unpack.
	Please see acceleration documentation for more details.
	'''

	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = acceleration('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System