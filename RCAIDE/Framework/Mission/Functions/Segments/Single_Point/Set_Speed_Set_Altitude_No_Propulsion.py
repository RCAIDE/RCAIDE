# RCAIDE/Library/Missions/Segments/Single_Point/Set_Speed_Set_Altitude_No_Propulsion.py
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
    A fixed speed and altitude

    Source:
    None

    Args:
    segment.altitude                               [meters]
    segment.air_speed                              [meters/second]
    segment.acceleration_z                         [meters/second^2]

    Returns:
    conditions.frames.inertial.acceleration_vector [meters/second^2]
    conditions.frames.inertial.velocity_vector     [meters/second]
    conditions.frames.inertial.position_vector     [meters]
    conditions.freestream.altitude                 [meters]
    conditions.frames.inertial.time                [seconds]


    """      
    
    # unpack
    alt             = segment.altitude
    air_speed       = segment.air_speed  
    sideslip        = segment.sideslip_angle
    acceleration_z  = segment.acceleration_z
    conditions      = segment.state.conditions 
    
    # check for initial altitude
    if alt is None:
        if not segment.state.initials: raise AttributeError('altitude not set')
        alt = -1.0 *segment.state.initials.conditions.frames.inertial.position_vector[-1,2]
     
    # pack
    conditions.freestream.altitude[:,0]             = alt
    conditions.frames.inertial.position_vector[:,2] = -alt 
    conditions.frames.inertial.velocity_vector[:,0] = np.cos(sideslip)*air_speed
    conditions.frames.inertial.velocity_vector[:,1] = np.sin(sideslip)*air_speed
    conditions.frames.inertial.acceleration_vector  = np.array([[0.0,0.0,acceleration_z]])   
     
