# RCAIDE/Library/Missions/Segments/Climb/Constant_Mach_Constant_Angle.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------  
#  IMPORT 
# ----------------------------------------------------------------------------------------------------------------------  
# import RCAIDE 
from RCAIDE.Framework.Mission.Functions.Common.Update.atmosphere import atmosphere

# package imports 
import RNUMPY as rp

# ----------------------------------------------------------------------------------------------------------------------  
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------  
def initialize_conditions(segment):
    """Sets the specified conditions which are given for the segment type.
    
    Assumptions:
    Constant Mach number, with a constant angle of climb

    Source:
    None

    Args:
    segment.climb_angle                                 [radians]
    segment.mach_number                                 [unitless]
    segment.altitude_start                              [meters]
    segment.altitude_end                                [meters]
    segment.state.numerics.dimensionless.control_points [unitless]
    conditions.freestream.density                       [kilograms/meter^3]

    Returns:
    conditions.frames.inertial.velocity_vector  [meters/second]
    conditions.frames.inertial.position_vector  [meters]
    conditions.freestream.altitude              [meters]


    """       
    # unpack User Inputs
    climb_angle = segment.climb_angle
    mach_number = segment.mach_number
    alt0        = segment.altitude_start 
    beta        = segment.sideslip_angle 
    conditions  = segment.state.conditions   
    
    # check for initial altitude
    if alt0 is None:
        if not segment.state.initials: raise AttributeError('initial altitude not set')
        alt0 = -1.0 * segment.state.initials.conditions.frames.inertial.position_vector[-1,2] 

    # check for initial velocity
    if mach_number is None: 
        if not segment.state.initials: raise AttributeError('mach not set')
        v_mag  = rp.linalg.norm(segment.state.initials.conditions.frames.inertial.velocity_vector[-1])*segment.state.ones_row(1)   
    else: 
        # Update freestream to get speed of sound
        atmosphere(segment)
        a = conditions.freestream.speed_of_sound    
        
        # process velocity vector
        v_mag = mach_number * a
    v_xy  = v_mag * rp.cos(climb_angle)
    v_z   = -v_mag * rp.sin(climb_angle)
    v_x   = rp.cos(beta)*v_xy
    v_y   = rp.sin(beta)*v_xy
    
    # pack conditions    
    conditions.freestream.altitude[:,0]              = -conditions.frames.inertial.position_vector[:,2]  
    conditions.frames.inertial.velocity_vector[:,0]  = v_x[:,0]
    conditions.frames.inertial.velocity_vector[:,1]  = v_y[:,0]
    conditions.frames.inertial.velocity_vector[:,2]  = v_z[:,0]   
    
# ----------------------------------------------------------------------------------------------------------------------  
#  Residual Total Forces
# ----------------------------------------------------------------------------------------------------------------------  
def altitude_residual(segment):
    
    # Unpack results   
    alt_in  = segment.state.unknowns.altitude[:,0] 
    alt_out = segment.state.conditions.freestream.altitude[:,0]     
    segment.state.residuals.altitude[:,0] = (alt_in - alt_out)/alt_out[-1]

    return    

# ----------------------------------------------------------------------------------------------------------------------  
# Update Differentials
# ----------------------------------------------------------------------------------------------------------------------     
def update_differentials(segment):
    """ On each iteration creates the differentials and integration functions from knowns about the problem. 
      Sets the time at each point. Must return in dimensional time, with t[0] = 0.
      This is different from the common method as it also includes the scaling of operators.

        Assumptions:
        Works with a segment discretized in vertical position, altitude

        Args:
        state.numerics.dimensionless.control_points      [unitless]
        state.numerics.dimensionless.differentiate       [unitless]
        state.numerics.dimensionless.integrate           [unitless]
        state.conditions.frames.inertial.position_vector [meter]
        state.conditions.frames.inertial.velocity_vector [meter/second]
        

        Returns:
        state.conditions.frames.inertial.time            [second]

    """    

    # unpack
    numerics   = segment.state.numerics
    conditions = segment.state.conditions
    x          = numerics.dimensionless.control_points
    D          = numerics.dimensionless.differentiate
    I          = numerics.dimensionless.integrate 
    r          = segment.state.conditions.frames.inertial.position_vector
    v          = segment.state.conditions.frames.inertial.velocity_vector
    alt0       = segment.altitude_start
    altf       = segment.altitude_end    

    # check for initial altitude
    if alt0 is None:
        if not segment.state.initials: raise AttributeError('initial altitude not set')
        alt0 = -1.0 * segment.state.initials.conditions.frames.inertial.position_vector[-1,2]
        
    dz = altf - alt0
    vz = -v[:,2,None] # maintain column array

    # get overall time step
    dt = (dz/rp.dot(I,vz))[-1]

    # rescale operators
    x = x * dt
    D = D / dt
    I = I * dt
    
    # Calculate the altitudes
    alt = rp.dot(I,vz) + alt0
    
    # pack
    t_initial                                       = segment.state.conditions.frames.inertial.time[0,0]
    numerics.time.control_points                    = x
    numerics.time.differentiate                     = D
    numerics.time.integrate                         = I
    conditions.frames.inertial.time[1:,0]           = t_initial + x[1:,0]
    conditions.frames.inertial.position_vector[:,2] = -alt[:,0]  
    conditions.freestream.altitude[:,0]             =  alt[:,0]  

    return