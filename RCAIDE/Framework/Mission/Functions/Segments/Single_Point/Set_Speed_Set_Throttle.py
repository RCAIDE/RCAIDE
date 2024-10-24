# RCAIDE/Library/Missions/Segments/Single_Point/Set_Speed_Set_Throttle.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team
 
# ----------------------------------------------------------------------------------------------------------------------  
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------  

import numpy as np

# ----------------------------------------------------------------------------------------------------------------------  
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------   
def initialize_conditions(segment):
    """Sets the specified conditions which are given for the segment type.

    Assumptions:
    A fixed speed and throttle

    Source:
    None

    Args:
    segment.altitude                               [meters]
    segment.air_speed                              [meters/second]
    segment.throttle                               [unitless]
    segment.acceleration_z                         [meters/second^2]
    segment.state.unknowns.acceleration            [meters/second^2]

    Returns:
    conditions.frames.inertial.acceleration_vector [meters/second^2]
    conditions.frames.inertial.velocity_vector     [meters/second]
    conditions.frames.inertial.position_vector     [meters]
    conditions.freestream.altitude                 [meters]
    conditions.frames.inertial.time                [seconds]


    """      
    
    # unpack
    alt              = segment.altitude
    air_speed        = segment.air_speed
    beta             = segment.sideslip_angle  
    acceleration_z   = segment.acceleration_z
    acceleration     = segment.state.unknowns.acceleration[0][0]
    
    # check for initial altitude
    if alt is None:
        if not segment.state.initials: raise AttributeError('altitude not set')
        alt = -1.0 *segment.state.initials.conditions.frames.inertial.position_vector[-1,2]
     
    # pack
    segment.state.conditions.freestream.altitude[:,0]             = alt
    segment.state.conditions.frames.inertial.position_vector[:,2] = -alt 
    segment.state.conditions.frames.inertial.velocity_vector[:,0] = np.cos(beta)*air_speed
    segment.state.conditions.frames.inertial.velocity_vector[:,1] = np.sin(beta)*air_speed
    segment.state.conditions.frames.inertial.acceleration_vector  = np.array([[acceleration,0.0,acceleration_z]]) 
    
# ----------------------------------------------------------------------------------------------------------------------  
#  Unpack Unknowns 
# ----------------------------------------------------------------------------------------------------------------------   
def unpack_unknowns(segment):
    """ Unpacks the x accleration and body angle from the solver to the mission
    
        Assumptions:
        None
        
        Args:
            segment.state.unknowns:
                acceleration                        [meters/second^2]
                body_angle                          [radians]
            
        Returns:
            segment.state.conditions:
                frames.inertial.acceleration_vector [meters/second^2]
                frames.body.inertial_rotations      [radians]
 
    """      
    
    # unpack unknowns
    acceleration  = segment.state.unknowns.acceleration
    body_angle    = segment.state.unknowns.body_angle
    
    # apply unknowns
    segment.state.conditions.frames.inertial.acceleration_vector[0,0] = acceleration
    segment.state.conditions.frames.body.inertial_rotations[:,1]      = body_angle[:,0]      