## @ingroup Library-Missions-Common Common-Update
# RCAIDE/Library/Missions/Common/Update/kinematics.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# package imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  Update Acceleration
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Missions-Segments-Common-Update
def kinematics(segment):
    """ Updates the kinematics of the rigid body (aircraft) 
        
        Assumptions:
            None
        
        Args:
            segment.state.:
                 conditions.frames.inertial.velocity_vector    [m/s]
                 numerics.time.differentiate                   [-]
                 
        Returns:
            segment.conditions 
                 frames.inertial.acceleration_vector  
    """   
    
    # unpack conditions
    v = segment.state.conditions.frames.inertial.velocity_vector
    D = segment.state.numerics.time.differentiate
    
    # accelerations
    acc = np.dot(D,v)
    
    # pack conditions
    segment.state.conditions.frames.inertial.acceleration_vector[:,:] = acc[:,:]   