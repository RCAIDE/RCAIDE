## @ingroup Library-Missions-Segments-Vertical_Flight
# RCAIDE/Library/Missions/Segments/Vertical_Flight/Descent.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 
 
# ----------------------------------------------------------------------------------------------------------------------  
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------  

## @ingroup Library-Missions-Segments-Vertical_Flight
def initialize_conditions(segment):
    """Sets the specified conditions which are given for the segment type.

    Assumptions:
    Descent segment with a constant rate.

    Source:
    None

    Args:
    segment.altitude_start                              [meters]
    segment.altitude_end                                [meters]
    segment.descent_rate                                [meters/second]
    segment.state.numerics.dimensionless.control_points [unitless]
    segment.state.conditions.frames.inertial.time       [seconds]

    Returns:
    conditions.frames.inertial.velocity_vector  [meters/second]
    conditions.frames.inertial.position_vector  [meters]
    conditions.freestream.altitude              [meters]
    conditions.frames.inertial.time             [seconds]


    """      
    
    # unpack
    descent_rate = segment.descent_rate
    alt0         = segment.altitude_start 
    altf         = segment.altitude_end
    t_nondim     = segment.state.numerics.dimensionless.control_points
    t_initial    = segment.state.conditions.frames.inertial.time[0,0]
    conditions   = segment.state.conditions  

    # check for initial altitude
    if alt0 is None:
        if not segment.state.initials: raise AttributeError('initial altitude not set')
        alt0 = -1.0 *segment.state.initials.conditions.frames.inertial.position_vector[-1,2]

    # discretize on altitude
    alt = t_nondim * (altf-alt0) + alt0
    
    # process velocity vector
    v_z = descent_rate     
    dt  = (alt0 - altf)/descent_rate

    # rescale operators
    t = t_nondim * dt

    # pack
    t_initial = segment.state.conditions.frames.inertial.time[0,0]
    segment.state.conditions.frames.inertial.time[:,0] = t_initial + t[:,0]    
    
    # pack conditions    
    conditions.frames.inertial.velocity_vector[:,0] = 0.
    conditions.frames.inertial.velocity_vector[:,2] = v_z
    conditions.frames.inertial.position_vector[:,2] = -alt[:,0] 
    conditions.freestream.altitude[:,0]             =  alt[:,0]
    conditions.frames.inertial.time[:,0]            = t_initial + t[:,0]