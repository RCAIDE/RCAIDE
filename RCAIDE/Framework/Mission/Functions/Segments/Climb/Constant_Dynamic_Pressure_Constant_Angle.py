# RCAIDE/Library/Missions/Segments/Climb/Constant_Dynamic_Pressure_Constant_Angle.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE  
from RCAIDE.Framework.Mission.Functions.Common.Update.atmosphere import atmosphere

# Package imports  
import numpy as np
 
# ----------------------------------------------------------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------
def initialize_conditions_unpack_unknowns(segment):
    """Sets the specified conditions which are given for the segment type. 
     Computed flight kinematics include: 
       conditions.frames.inertial.velocity_vector  [meters/second]
       conditions.frames.inertial.position_vector  [meters]
       conditions.energy.throttle              [unitless]
       conditions.frames.body.inertial_rotations   [radians]


    Assumptions:
       Constrant dynamic pressure and constant rate of climb

    Source:
       None

    Args:
       segment.climb_angle                                 [radians]
       segment.dynamic_pressure                            [pascals]
       segment.altitude_start                              [meters]
       segment.altitude_end                                [meters]
       segment.state.numerics.dimensionless.control_points [unitless]
       conditions.freestream.density                       [kilograms/meter^3]  

    Returns:
       None 

    """           
    
    # unpack
    climb_angle = segment.climb_angle
    q           = segment.dynamic_pressure
    alt0        = segment.altitude_start  
    conditions  = segment.state.conditions
    beta        = segment.sideslip_angle
    rho         = conditions.freestream.density[:,0]  
    
    # unpack unknowns  
    alts     = conditions.frames.inertial.position_vector[:,2]

    # Update freestream to get density
    atmosphere(segment)
    rho = conditions.freestream.density[:,0]   

    # check for initial altitude
    if alt0 is None:
        if not segment.state.initials: raise AttributeError('initial altitude not set')
        alt0 = -1.0 * segment.state.initials.conditions.frames.inertial.position_vector[-1,2] 

    # check for initial velocity
    if q is None: 
        if not segment.state.initials: raise AttributeError('dynamic pressure not set')
        v_mag = np.linalg.norm(segment.state.initials.conditions.frames.inertial.velocity_vector[-1])
    else:  
        # process velocity vector
        v_mag = np.sqrt(2*q/rho)
        
    v_x   = np.cos(beta)*v_mag * np.cos(climb_angle)
    v_y   = np.sin(beta)*v_mag * np.cos(climb_angle)
    v_z   = -v_mag * np.sin(climb_angle)
    
    # pack conditions    
    conditions.freestream.altitude[:,0]             =  -alts      
    conditions.frames.inertial.velocity_vector[:,0] = v_x
    conditions.frames.inertial.velocity_vector[:,1] = v_y
    conditions.frames.inertial.velocity_vector[:,2] = v_z   
    
def residual_altitude(segment):
    """Computes the altitude residual

    Assumptions:
    No higher order terms.

    Source:
    None

    Args:
    segment.state.conditions.frames.inertial.total_force_vector   [Newtons]
    segment.state.conditions.frames.inertial.acceleration_vector  [meter/second^2]
    segment.state.conditions.weights.total_mass                   [kilogram]
    segment.state.conditions.freestream.altitude                  [meter]

    Returns:
    segment.state.residuals.altitude                              [meters] 


    """     
    
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
    dt = (dz/np.dot(I,vz))[-1]

    # rescale operators
    x = x * dt
    D = D / dt
    I = I * dt
    
    # Calculate the altitudes
    alt = np.dot(I,vz) + alt0
    
    # pack
    t_initial                                       = segment.state.conditions.frames.inertial.time[0,0]
    numerics.time.control_points                    = x
    numerics.time.differentiate                     = D
    numerics.time.integrate                         = I
    conditions.frames.inertial.time[1:,0]           = t_initial + x[1:,0]
    conditions.frames.inertial.position_vector[:,2] = -alt[:,0]  
    conditions.freestream.altitude[:,0]             =  alt[:,0]  

    return