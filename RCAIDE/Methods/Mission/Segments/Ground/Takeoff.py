## @ingroup Methods-Missions-Segments-Ground
# RCAIDE/Methods/Missions/Segments/Ground/Takeoff.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE Imports 

import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
# unpack unknowns
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Missions-Segments-Ground
def initialize_conditions(segment):
    """Sets the specified conditions which are given for the segment type.

    Assumptions:
    Builds on the initialize conditions for common

    Source:
    N/A

    Inputs:
    segment.throttle                           [unitless]
    conditions.frames.inertial.position_vector [meters]
    conditions.weights.total_mass              [kilogram]

    Outputs:
    conditions.weights.total_mass              [kilogram]
    conditions.frames.inertial.position_vector [unitless]
    conditions.propulsion.throttle             [meters]
    
    Properties Used:
    N/A
    """  

    # use the common initialization # unpack inputs
    alt      = segment.altitude 
    v0       = segment.velocity_start
    vf       = segment.velocity_end 
    throttle = segment.throttle	
    
    # check for initial altitude
    if alt is None:
        if not segment.state.initials: raise AttributeError('altitude not set')
        alt = -1.0 *segment.state.initials.conditions.frames.inertial.position_vector[-1,2]   

    if v0  is None: 
        v0 = np.linalg.norm(segment.state.initials.conditions.frames.inertial.velocity_vector[-1])
        
    # avoid having zero velocity since aero and propulsion models need non-zero Reynolds number
    if v0 == 0.0: v0 = 0.01
    if vf == 0.0: vf = 0.01
    
    # intial and final speed cannot be the same
    if v0 == vf:
        vf = vf + 0.01
        
    # repack
    segment.air_speed_start = v0
    segment.air_speed_end   = vf
    
    initialized_velocity = (vf - v0)*segment.state.numerics.dimensionless.control_points + v0
    
    # Initialize the x velocity unknowns to speed convergence:
    segment.state.unknowns.velocity_x = initialized_velocity[1:,0]    

    # pack conditions 
    segment.state.conditions.frames.inertial.velocity_vector[:,0] = initialized_velocity[:,0]
    segment.state.conditions.ground.incline[:,0]                  = segment.ground_incline
    segment.state.conditions.ground.friction_coefficient[:,0]     = segment.friction_coefficient
    segment.state.conditions.propulsion.throttle[:,0]             = throttle  
    segment.state.conditions.freestream.altitude[:,0]             = alt
    segment.state.conditions.frames.inertial.position_vector[:,2] = -alt  
    conditions = segment.state.conditions    
    
    # unpack
    throttle  = segment.throttle	
    r_initial = conditions.frames.inertial.position_vector[0,:][None,:]
    m_initial = segment.analyses.weights.vehicle.mass_properties.takeoff    

    # default initial time, position, and mass
    # apply initials
    conditions.weights.total_mass[:,0]              = m_initial
    conditions.frames.inertial.position_vector[:,:] = r_initial[:,:]
    conditions.propulsion.throttle[:,0]             = throttle