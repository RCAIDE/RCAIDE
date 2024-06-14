## @ingroup Library-Missions-Segments-Descent
# RCAIDE/Library/Missions/Segments/Descent/Constant_Speed_Constant_Rate.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------  
#  IMPORT 
# ----------------------------------------------------------------------------------------------------------------------  
# package imports 
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Missions-Segments-Descent
def initialize_conditions(segment):
    """Sets the specified conditions which are given for the segment type.

    Assumptions:
    Constant speed and constant descent rate

    Source:
    N/A

    Inputs:
    segment.descent_rate                                [meters/second]
    segment.altitude_start                              [meters]
    segment.altitude_end                                [meters]
    segment.air_speed                                   [meters/second]
    segment.state.numerics.dimensionless.control_points [array]

    Outputs:
    conditions.frames.inertial.velocity_vector  [meters/second]
    conditions.frames.inertial.position_vector  [meters]
    conditions.freestream.altitude              [meters]
    conditions.frames.inertial.time             [seconds]

    Properties Used:
    N/A
    """     
    
    # unpack
    descent_rate = segment.descent_rate
    air_speed    = segment.air_speed   
    alt0         = segment.altitude_start 
    altf         = segment.altitude_end
    beta         = segment.sideslip_angle
    t_nondim     = segment.state.numerics.dimensionless.control_points
    conditions   = segment.state.conditions  

    # check for initial altitude
    if alt0 is None:
        if not segment.state.initials: raise AttributeError('initial altitude not set')
        alt0 = -1.0 *segment.state.initials.conditions.frames.inertial.position_vector[-1,2] 
        
    # check for initial velocity vector
    if air_speed is None:
        if not segment.state.initials: raise AttributeError('initial airspeed not set')
        air_speed  =  np.linalg.norm(segment.state.initials.conditions.frames.inertial.velocity_vector[-1,:])   
            
    # discretize on altitude
    alt = t_nondim * (altf-alt0) + alt0
    
    # process velocity vector
    v_xy_mag    = air_speed
    v_z         = descent_rate # z points down
    v_xy        = np.sqrt(v_xy_mag**2 - v_z**2 )
    v_x         = np.cos(beta)*v_xy
    v_y         = np.sin(beta)*v_xy
    
    # pack conditions    
    conditions.frames.inertial.velocity_vector[:,0] = v_x
    conditions.frames.inertial.velocity_vector[:,1] = v_y
    conditions.frames.inertial.velocity_vector[:,2] = v_z
    conditions.frames.inertial.position_vector[:,2] = -alt[:,0] # z points down
    conditions.freestream.altitude[:,0]             =  alt[:,0] # positive altitude in this context