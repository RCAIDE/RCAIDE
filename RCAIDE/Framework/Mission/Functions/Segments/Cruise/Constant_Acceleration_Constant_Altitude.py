# RCAIDE/Library/Missions/Segments/Cruise/Constant_Acceleration_Constant_Altitude.py
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
    Constant acceleration and constant altitude

    Source:
    None

    Args:
    segment.altitude                [meters]
    segment.air_speed_start         [meters/second]
    segment.air_speed_end           [meters/second]
    segment.acceleration            [meters/second^2]
    conditions.frames.inertial.time [seconds]

    Returns:
    conditions.frames.inertial.velocity_vector  [meters/second]
    conditions.frames.inertial.position_vector  [meters]
    conditions.freestream.altitude              [meters]
    conditions.frames.inertial.time             [seconds]


    """      
    
    # unpack
    alt        = segment.altitude 
    v0         = segment.air_speed_start
    vf         = segment.air_speed_end
    ax         = segment.acceleration    
    beta       = segment.sideslip_angle
    conditions = segment.state.conditions 
    
    # check for initial altitude
    if alt is None:
        if not segment.state.initials: raise AttributeError('altitude not set')
        alt = -1.0 * segment.state.initials.conditions.frames.inertial.position_vector[-1,2]
    
    # check for initial velocity
    if v0 is None: 
        if not segment.state.initials: raise AttributeError('airspeed not set')
        v0 = rp.linalg.norm(segment.state.initials.conditions.frames.inertial.velocity_vector[-1])
        
    # dimensionalize time
    t_initial = conditions.frames.inertial.time[0,0]
    t_final   = (vf-v0)/ax + t_initial
    t_nondim  = segment.state.numerics.dimensionless.control_points
    time      = t_nondim * (t_final-t_initial) + t_initial 
    v_mag     = v0+(time - t_initial)*ax
    v_x       = rp.cos(beta)*v_mag
    v_y       = rp.sin(beta)*v_mag
    
    # pack
    segment.state.conditions.freestream.altitude[:,0]             = alt
    segment.state.conditions.frames.inertial.position_vector[:,2] = -alt 
    segment.state.conditions.frames.inertial.velocity_vector[:,0] = v_x[:,0]
    segment.state.conditions.frames.inertial.velocity_vector[:,1] = v_y[:,0]
    segment.state.conditions.frames.inertial.time[:,0]            = time[:,0] 
