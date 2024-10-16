# RCAIDE/Library/Missions/Common/Update/inertial_horizontal_position.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# Package imports 
import RNUMPY as rp

# ----------------------------------------------------------------------------------------------------------------------
#  Integrate Position
# ---------------------------------------------------------------------------------------------------------------------- 
def inertial_horizontal_position(segment):
    """ Determines how far the airplane has traveled. 
    
        Assumptions:
        Assumes a flat earth, this is planar motion.
        
        Args:
            segment.state.conditions:
                frames.inertial.position_vector [meters]
                frames.inertial.velocity_vector [meters/second]
            segment.state.numerics.time.integrate       [float]
            
        Returns:
            segment.state.conditions:           
                frames.inertial.position_vector [meters] 
    """        

    conditions = segment.state.conditions
    psi        = segment.true_course       # sign convetion is clockwise positive
    cpts       = int(segment.state.numerics.number_of_control_points)
    x0         = conditions.frames.inertial.position_vector[0,None,0:1+1]
    R0         = conditions.frames.inertial.aircraft_range[0,None,0:1+1]
    vx         = conditions.frames.inertial.velocity_vector[:,0:1+1]
    I          = segment.state.numerics.time.integrate  
    trajectory = rp.repeat( rp.atleast_2d(rp.array([rp.cos(psi),rp.sin(psi)])),cpts , axis = 0) 
    
    # integrate
    x = rp.dot(I,vx)  
    x[:,1] = x[:,0]
    
    # pack
    conditions.frames.inertial.position_vector[:,0:1+1] = x0 + x[:,:]*trajectory
    conditions.frames.inertial.aircraft_range[:,0]      = R0 + x[:,0]  
    
    return