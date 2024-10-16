# RCAIDE/Library/Missions/Common/Update/angular_acceleration.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 
import RNUMPY as rp

# ----------------------------------------------------------------------------------------------------------------------
# Update Acceleration
# ----------------------------------------------------------------------------------------------------------------------   
def angular_acceleration(segment):
    """ Differentiates the angular velocity vector to get angular accelerations
    
        Assumptions:
        Assumes a flat earth, this is planar motion.
        
        Args:
            segment.state.conditions:
                frames.inertial.angular_velocity_vector     [rad/second]
            segment.state.numerics.time.differentiate       [float]
            
        Returns:
            segment.state.conditions:           
                frames.inertial.angular_acceleration_vector [rad/s^2] 
    """            
    
    # unpack conditions
    omega = segment.state.conditions.frames.inertial.angular_velocity_vector
    D     = segment.state.numerics.time.differentiate
    
    # accelerations
    ang_acc = rp.dot(D,omega)
    
    # pack conditions
    segment.state.conditions.frames.inertial.angular_acceleration_vector[:,:] = ang_acc[:,:]   