## @ingroup Library-Missions-Common Common-Update
# RCAIDE/Library/Missions/Common/Update/curvilinear_inertial_horizontal_position.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# Package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Integrate Position
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Missions-Common-Update 
def curvilinear_inertial_horizontal_position(segment):
    """ Determines how far the airplane has traveled. 
    
        Assumptions:
        Assumes a flat earth, this is planar motion.
        
        Inputs:
            segment.state.conditions:
                frames.inertial.position_vector [meters]
                frames.inertial.velocity_vector [meters/second]
            segment.state.numerics.time.integrate       [float]
            
        Outputs:
            segment.state.conditions:           
                frames.inertial.position_vector [meters]

        Properties Used:
        N/A
                                
    """        

    conditions = segment.state.conditions  
    x0         = conditions.frames.inertial.position_vector[0, 0]
    y0         = conditions.frames.inertial.position_vector[0, 1]
    R0         = conditions.frames.inertial.aircraft_range[0,None,0:1+1]
    vx         = conditions.frames.inertial.velocity_vector[:,0:1+1]
    I          = segment.state.numerics.time.integrate 
    R          = segment.turn_radius
    sign       = np.sign(segment.turn_angle)
    
    # integrate
    arc_length = np.dot(I,vx)
    
    theta = arc_length[:,0]/R
    
    delta_x = sign * R * np.sin(theta)
    delta_y = R * (1 - np.cos(theta))
    
    # pack
    conditions.frames.inertial.position_vector[:,0] = x0 + delta_x 
    conditions.frames.inertial.position_vector[:,1] = y0 - sign * delta_y 
    conditions.frames.inertial.aircraft_range[:,0]  = R0 + arc_length[:,0]  
    
    return