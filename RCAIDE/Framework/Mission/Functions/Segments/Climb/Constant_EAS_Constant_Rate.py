# RCAIDE/Library/Missions/Segments/Climb/Constant_EAS_Constant_Rate.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE 
from RCAIDE.Framework.Mission.Functions.Common.Update.atmosphere import atmosphere

# Package imports  
import RNUMPY as rp
 
# ----------------------------------------------------------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------
def initialize_conditions(segment):
    """Sets the specified conditions which are given for the segment type.
    
    Assumptions:
    Constant true airspeed with a constant rate of climb

    Source:
    None

    Args:
    segment.climb_rate                                  [meters/second]
    segment.equivalent_air_speed                        [meters/second]
    segment.altitude_start                              [meters]
    segment.altitude_end                                [meters]
    segment.state.numerics.dimensionless.control_points [unitless]
    conditions.freestream.density                       [kilograms/meter^3]

    Returns:
    conditions.frames.inertial.velocity_vector  [meters/second]
    conditions.frames.inertial.position_vector  [meters]
    conditions.freestream.altitude              [meters]


    """         
    
    # unpack
    climb_rate = segment.climb_rate
    eas        = segment.equivalent_air_speed    
    beta       = segment.sideslip_angle
    alt0       = segment.altitude_start 
    altf       = segment.altitude_end
    t_nondim   = segment.state.numerics.dimensionless.control_points
    conditions = segment.state.conditions  

    # check for initial altitude
    if alt0 is None:
        if not segment.state.initials: raise AttributeError('initial altitude not set')
        alt0 = -1.0 * segment.state.initials.conditions.frames.inertial.position_vector[-1,2]

    # discretize on altitude
    alt = t_nondim * (altf-alt0) + alt0
     
    # check for initial velocity vector
    if eas is None:
        if not segment.state.initials: raise AttributeError('initial equivalent airspeed not set')
        air_speed  = rp.linalg.norm(segment.state.initials.conditions.frames.inertial.velocity_vector[-1,:])  
    else: 
        # determine airspeed from equivalent airspeed
        atmosphere(segment) # get density for airspeed
        density   = conditions.freestream.density[:,0]   
        MSL_data  = segment.analyses.atmosphere.compute_values(0.0,0.0)
        air_speed = eas/rp.sqrt(density/MSL_data.density[0])    
    
    # process velocity vector
    v_mag  = air_speed
    v_z    = -climb_rate 
    v_xy   = rp.sqrt( v_mag**2 - v_z**2 )
    v_x    = rp.cos(beta)*v_xy
    v_y    = rp.sin(beta)*v_xy
    
    # pack conditions    
    conditions.freestream.altitude[:,0]             =  alt[:,0]  
    conditions.frames.inertial.velocity_vector[:,0] = v_x
    conditions.frames.inertial.velocity_vector[:,1] = v_y
    conditions.frames.inertial.velocity_vector[:,2] = v_z
    conditions.frames.inertial.position_vector[:,2] = -alt[:,0] 