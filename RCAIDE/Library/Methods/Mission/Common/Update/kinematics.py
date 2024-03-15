## @ingroup Library-Methods-Mission-Common Common-Update
# RCAIDE/Library/Methods/Missions/Common/Update/kinematics.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# package imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Update Acceleration
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Mission-Segments-Common-Update
def kinematics(segment):
    """ Updates the kinematics of the rigid body (aircraft) 
        
        Assumptions:
        N/A
        
        Inputs:
            segment.state.:
                 conditions.frames.inertial.velocity_vector    [m/s]
                 numerics.time.differentiate                   [-]
                 
        Outputs:
            segment.conditions 
                 frames.inertial.acceleration_vector 
      
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


def _kinematics(State, Settings, System):
	'''
	Framework version of kinematics.
	Wraps kinematics with State, Settings, System pack/unpack.
	Please see kinematics documentation for more details.
	'''

	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = kinematics('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System