# RCAIDE/Library/Missions/Segments/Climb/Constant_Mach_Constant_Rate.py
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
def initialize_conditions(segment):
    """Sets the specified conditions which are given for the segment type.
    
    Assumptions:
    Constant Mach number, with a constant rate of climb

    Source:
    None

    Args:
    segment.climb_rate                                  [meters/second]
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
    
    # unpack 
    climb_rate  = segment.climb_rate
    mach_number = segment.mach_number
    alt0        = segment.altitude_start 
    altf        = segment.altitude_end
    beta        = segment.sideslip_angle
    t_nondim    = segment.state.numerics.dimensionless.control_points
    conditions  = segment.state.conditions  

    # check for initial altitude
    if alt0 is None:
        if not segment.state.initials: raise AttributeError('initial altitude not set')
        alt0 = -1.0 * segment.state.initials.conditions.frames.inertial.position_vector[-1,2]

    # discretize on altitude
    alt = t_nondim * (altf-alt0) + alt0
    
    # Update freestream to get speed of sound
    atmosphere(segment)
    a = conditions.freestream.speed_of_sound    

    # check for initial velocity
    if mach_number is None: 
        if not segment.state.initials: raise AttributeError('mach not set')
        v_mag = np.linalg.norm(segment.state.initials.conditions.frames.inertial.velocity_vector[-1])   
    else: 
        # process velocity vector
        v_mag = mach_number * a
    v_z   = -climb_rate 
    v_xy  = np.sqrt( v_mag**2 - v_z**2 )
    v_x   = np.cos(beta)*v_xy
    v_y   = np.sin(beta)*v_xy 
    
    # pack conditions    
    conditions.freestream.altitude[:,0]             =  alt[:,0]
    conditions.frames.inertial.velocity_vector[:,0] = v_x[:,0]
    conditions.frames.inertial.velocity_vector[:,1] = v_y[:,0]
    conditions.frames.inertial.velocity_vector[:,2] = v_z
    conditions.frames.inertial.position_vector[:,2] = -alt[:,0] 
    conditions.freestream.altitude[:,0]             =  alt[:,0] 