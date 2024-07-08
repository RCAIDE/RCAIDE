# RCAIDE/Library/Missions/Common/Update/acceleration.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# Update Acceleration
# ----------------------------------------------------------------------------------------------------------------------   
def acceleration(segment):
    """ Differentiates the velocity vector to get accelerations.
    
        Assumptions:
            Assumes a flat earth, this is planar motion.
        
        Args:
            segment.state.conditions.frames.inertial.velocity_vector     [meters/second]
            segment.state.numerics.time.differentiate                    [float]
            
        Returns:
            None
    """    
    # unpack conditions
    v = segment.state.conditions.frames.inertial.velocity_vector
    D = segment.state.numerics.time.differentiate
    
    # accelerations
    acc = np.dot(D,v)
    
    # pack conditions
    segment.state.conditions.frames.inertial.acceleration_vector[:,:] = acc[:,:]   