# RCAIDE/Library/Missions/Segments/Climb/Constant_Throttle_Constant_Speed.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# Package imports  
import numpy as np
 
# ----------------------------------------------------------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------
def unpack_body_angle(segment):
    """Unpacks and sets the proper value for body angle

    Assumptions:
    None

    Source:
    None

    Args:
    state.unknowns.body_angle                      [Radians]

    Returns:
    state.conditions.frames.body.inertial_rotation [Radians]


    """          

    # unpack unknowns
    theta      = segment.state.unknowns.body_angle 
    segment.state.conditions.frames.body.inertial_rotations[:,1] = theta[:,0]      


# ----------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------

def initialize_conditions(segment):
    """Sets the specified conditions which are given for the segment type.
    
    Assumptions:
    Constant throttle estting, with a constant true airspeed

    Source:
    None

    Args:
    segment.air_speed                                   [meters/second] 
    segment.altitude_start                              [meters]
    segment.altitude_end                                [meters]
    segment.state.numerics.dimensionless.control_points [unitless]
    conditions.freestream.density                       [kilograms/meter^3]

    Returns:
    conditions.frames.inertial.velocity_vector          [meters/second]
    conditions.energy.throttle                          [unitless]


    """         
    
    # unpack 
    air_speed  = segment.air_speed   
    alt0       = segment.altitude_start 
    conditions = segment.state.conditions  

    # check for initial altitude
    if alt0 is None:
        if not segment.state.initials: raise AttributeError('initial altitude not set')
        alt0 = -1.0 *segment.state.initials.conditions.frames.inertial.position_vector[-1,2]

    # pack conditions   
    conditions.frames.inertial.velocity_vector[:,0] = air_speed # start up value

def update_differentials_altitude(segment):
    """On each iteration creates the differentials and integration funcitons from knowns about the problem. Sets the time at each point. Must return in dimensional time, with t[0] = 0
    
    Assumptions:
    Constant throttle setting, with a constant true airspeed.

    Source:
    None

    Args:
    segment.climb_angle                         [radians]
    state.conditions.frames.inertial.velocity_vector [meter/second]
    segment.altitude_start                      [meters]
    segment.altitude_end                        [meters]

    Returns:
    state.conditions.frames.inertial.time       [seconds]
    conditions.frames.inertial.position_vector  [meters]
    conditions.freestream.altitude              [meters]


    """   

    # unpack
    t = segment.state.numerics.dimensionless.control_points
    I = segment.state.numerics.dimensionless.integrate 
    
    # Unpack segment initials
    alt0       = segment.altitude_start 
    altf       = segment.altitude_end    
    conditions = segment.state.conditions  
    v          = segment.state.conditions.frames.inertial.velocity_vector
    
    # check for initial altitude
    if alt0 is None:
        if not segment.state.initials: raise AttributeError('initial altitude not set')
        alt0 = -1.0 *segment.state.initials.conditions.frames.inertial.position_vector[-1,2]    
    
    # get overall time step
    vz = -v[:,2,None] # Inertial velocity is z down
    dz = altf- alt0    
    dt = dz / np.dot(I[-1,:],vz)[-1] # maintain column array
    
    # Integrate vz to get altitudes
    alt = alt0 + np.dot(I*dt,vz)

    # rescale operators
    t = t * dt

    # pack 
    segment.state.conditions.frames.inertial.time[:,0] = segment.state.conditions.frames.inertial.time[0,0] + t[:,0]
    conditions.frames.inertial.position_vector[:,2]    = -alt[:,0] 
    conditions.freestream.altitude[:,0]                =  alt[:,0]     

    return

# ----------------------------------------------------------------------
#  Update Velocity Vector from Wind Angle
# ----------------------------------------------------------------------

def update_velocity_vector_from_wind_angle(segment):
    
    # unpack
    conditions = segment.state.conditions 
    v_mag      = segment.air_speed 
    beta       = segment.sideslip_angle
    alpha      = segment.state.unknowns.wind_angle[:,0][:,None]
    theta      = segment.state.unknowns.body_angle[:,0][:,None]
    
    # Flight path angle
    gamma = theta-alpha

    # process
    v_x =   np.cos(beta) *v_mag * np.cos(gamma)
    v_y =   np.sin(beta) *v_mag * np.cos(gamma)
    v_z = -v_mag * np.sin(gamma) 

    # pack
    conditions.frames.inertial.velocity_vector[:,0] = v_x[:,0]
    conditions.frames.inertial.velocity_vector[:,1] = v_y[:,0]
    conditions.frames.inertial.velocity_vector[:,2] = v_z[:,0]

    return conditions
