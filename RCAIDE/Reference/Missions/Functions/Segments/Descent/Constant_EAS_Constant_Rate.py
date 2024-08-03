# RCAIDE/Library/Missions/Segments/Descent/Constant_EAS_Constant_Rate.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------  
#  IMPORT 
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports  
from RCAIDE.Reference.Missions.Functions.Common.Update.atmosphere import atmosphere

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------  
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------  
def initialize_conditions(segment):
    """Sets the specified conditions which are given for the segment type.

    Assumptions:
    Constant EAS speed and constant descent rate

    Source:
    None

    Args:
    segment.equivalent_air_speed                        [meters/second]
    segment.altitude_start                              [meters]
    segment.altitude_end                                [meters]
    segment.descent_rate                                [meters/second]
    segment.state.numerics.dimensionless.control_points [array]

    Returns:
    conditions.frames.inertial.velocity_vector  [meters/second]
    conditions.frames.inertial.position_vector  [meters]
    conditions.freestream.altitude              [meters]
    conditions.frames.inertial.time             [seconds]


    """       
    
    # unpack
    descent_rate = segment.descent_rate
    eas          = segment.equivalent_air_speed   
    alt0         = segment.altitude_start 
    altf         = segment.altitude_end 
    beta         = segment.sideslip_angle
    t_nondim     = segment.state.numerics.dimensionless.control_points
    conditions   = segment.state.conditions  

    # check for initial altitude
    if alt0 is None:
        if not segment.state.initials: raise AttributeError('initial altitude not set')
        alt0 = -1.0 * segment.state.initials.conditions.frames.inertial.position_vector[-1,2]


    # discretize on altitude
    alt = t_nondim * (altf-alt0) + alt0
    
    # Pack altitude before updating atmosphere
    conditions.freestream.altitude[:,0]             =  alt[:,0]     
    # determine airspeed from equivalent airspeed
    atmosphere(segment)  
    density   = conditions.freestream.density[:,0]   
    MSL_data  = segment.analyses.atmosphere.compute_values(0.0,0.0)

    # check for initial velocity vector
    if eas is None:
        if not segment.state.initials: raise AttributeError('initial equivalent airspeed not set')
        air_speed  = np.linalg.norm(segment.state.initials.conditions.frames.inertial.velocity_vector[-1,:])  
    else: 
        air_speed  = eas/np.sqrt(density/MSL_data.density[0])    
    
    # process velocity vector
    v_mag = air_speed
    v_z   = descent_rate 
    v_xy  = np.sqrt( v_mag**2 - v_z**2 )
    v_x   = np.cos(beta)*v_xy
    v_y   = np.sin(beta)*v_xy
    
    # pack conditions    
    conditions.frames.inertial.velocity_vector[:,0] = v_x
    conditions.frames.inertial.velocity_vector[:,1] = v_y
    conditions.frames.inertial.velocity_vector[:,2] = v_z
    conditions.frames.inertial.position_vector[:,2] = -alt[:,0] 
