# RCAIDE/Library/Missions/Segments/Climb/Constant_Speed_Linear_Altitude.py 
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# Package imports  
import RNUMPY as rp
 
# ----------------------------------------------------------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------
def initialize_conditions(segment):
    """Sets the specified conditions which are given for the segment type.

    Assumptions:
    Constrant dynamic pressure and constant rate of climb

    Source:
    None

    Args:
    segment.air_speed                           [meters/second]
    segment.altitude_start                      [meters]
    segment.altitude_end                        [meters]
    segment.distance                            [meters]

    Returns:
    conditions.frames.inertial.velocity_vector  [meters/second]
    conditions.frames.inertial.position_vector  [meters]
    conditions.freestream.altitude              [meters]
    conditions.frames.inertial.time             [seconds]


    """        
    
    # unpack
    alt0       = segment.altitude_start 
    altf       = segment.altitude_end
    xf         = segment.distance
    air_speed  = segment.air_speed    
    beta       = segment.sideslip_angle    
    conditions = segment.state.conditions 

    # check for initial velocity
    if air_speed is None: 
        if not segment.state.initials: raise AttributeError('airspeed not set')
        air_speed = rp.linalg.norm(segment.state.initials.conditions.frames.inertial.velocity_vector[-1])
        
    # check for initial altitude
    if alt0 is None:
        if not segment.state.initials: raise AttributeError('altitude not set')
        alt0 = -1.0 *segment.state.initials.conditions.frames.inertial.position_vector[-1,2]
     
    climb_angle  = rp.arctan((altf-alt0)/xf)
    v_x          = rp.cos(beta)*rp.cos(climb_angle)*air_speed
    v_y          = rp.sin(beta)*rp.cos(climb_angle)*air_speed
    v_z          = rp.sin(climb_angle)*air_speed 
    t_nondim     = segment.state.numerics.dimensionless.control_points
    
    # discretize on altitude
    alt = t_nondim * (altf-alt0) + alt0    
    
    # pack
    conditions.freestream.altitude[:,0]             = alt[:,0]
    conditions.frames.inertial.position_vector[:,2] = -alt[:,0]  
    conditions.frames.inertial.velocity_vector[:,0] = v_x
    conditions.frames.inertial.velocity_vector[:,1] = v_y
    conditions.frames.inertial.velocity_vector[:,2] = -v_z  