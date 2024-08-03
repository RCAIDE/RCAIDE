# RCAIDE/Library/Missions/Segments/Cruise/Constant_Mach_Constant_Altitude.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE   
from RCAIDE.Reference.Missions.Functions.Common.Update.atmosphere import atmosphere

# Package imports  
import numpy as np
 
# ----------------------------------------------------------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------
def initialize_conditions(segment):
    """Sets the specified conditions which are given for the segment type.

    Assumptions:
    Constant mach and constant altitude

    Source:
    None

    Args:
    segment.altitude                [meters]
    segment.distance                [meters]
    segment.mach_number             [unitless]

    Returns:
    conditions.frames.inertial.velocity_vector  [meters/second]
    conditions.frames.inertial.position_vector  [meters]
    conditions.freestream.altitude              [meters]
    conditions.frames.inertial.time             [seconds]


    """      
    
    # unpack
    alt        = segment.altitude
    xf         = segment.distance
    mach       = segment.mach_number
    beta       = segment.sideslip_angle
    conditions = segment.state.conditions    
    
    # check for initial altitude
    if alt is None:
        if not segment.state.initials: raise AttributeError('altitude not set')
        alt = -1.0 * segment.state.initials.conditions.frames.inertial.position_vector[-1,2]    
    segment.state.conditions.freestream.altitude[:,0] = alt
    
    # Update freestream to get speed of sound
    atmosphere(segment)
    a          = conditions.freestream.speed_of_sound       

    # check for initial velocity
    if mach is None: 
        if not segment.state.initials: raise AttributeError('airspeed not set')
        air_speed = np.linalg.norm(segment.state.initials.conditions.frames.inertial.velocity_vector[-1])    
    else: # compute speed, constant with constant altitude
        air_speed = mach * a
    
    # dimensionalize time
    t_initial = conditions.frames.inertial.time[0,0]
    t_final   = xf / air_speed + t_initial
    t_nondim  = segment.state.numerics.dimensionless.control_points
    time      =  t_nondim * (t_final-t_initial) + t_initial
    v_x       = np.cos(beta)*air_speed 
    v_y       = np.sin(beta)*air_speed 
    
    # pack
    segment.state.conditions.freestream.altitude[:,0]             = alt
    segment.state.conditions.frames.inertial.position_vector[:,2] = -alt 
    segment.state.conditions.frames.inertial.velocity_vector[:,0] = v_x[:,0]
    segment.state.conditions.frames.inertial.velocity_vector[:,1] = v_y[:,0]
    segment.state.conditions.frames.inertial.time[:,0]            = time[:,0]
    
