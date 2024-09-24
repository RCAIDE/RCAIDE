## @ingroup Library-Missions-Segments-Cruise
# RCAIDE/Library/Missions/Segments/Cruise/Curved_Constant_Radius_Constant_Speed_Constant_Altitude/initialize_conditions.py
# 
# 
# Created:  September 2024, A. Molloy + M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# Package imports 
import numpy as np
 
# ----------------------------------------------------------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Missions-Segments-Cruise
def initialize_conditions(segment):
    """Sets the specified conditions which are given for the segment type.

    Assumptions:
    Curved segment with constant radius, constant speed and constant altitude

    Source:
    N/A

    Inputs:
    segment.altitude                [meters] # deleted segment distance as it is now defined by the turn_angle and radius.
    segment.speed                   [meters/second]
    self.start_true_course          [degrees] true course of the vehicle before the turn
    self.turn_angle                 [degrees] angle measure of the curve. + is right hand turn, - is left hand turn. 
    self.radius                     [meters] radius of the turn
    
    Outputs: ***pretty sure that no additional outputs are need. Verify this***
    conditions.frames.inertial.velocity_vector  [meters/second]
    conditions.frames.inertial.position_vector  [meters]
    conditions.freestream.altitude              [meters]
    conditions.frames.inertial.time             [seconds]

    Properties Used:
    N/A
    """        
    
    # unpack 
    alt               = segment.altitude
    air_speed         = segment.air_speed       
    beta              = segment.sideslip_angle
    radius            = segment.turn_radius
    start_true_course = segment.start_true_course
    arc_sector        = segment.turn_angle
    conditions        = segment.state.conditions 

    # check for initial velocity
    if air_speed is None: 
        if not segment.state.initials: raise AttributeError('airspeed not set')
        air_speed = np.linalg.norm(segment.state.initials.conditions.frames.inertial.velocity_vector[-1])
        
    # check for initial altitude
    if alt is None:
        if not segment.state.initials: raise AttributeError('altitude not set')
        alt = -1.0 * segment.state.initials.conditions.frames.inertial.position_vector[-1,2]
    
    # check for initial altitude
    if radius is None:
        if not segment.state.initials: raise AttributeError('radius not set')
        radius = 0.1 # minimum radius so as to approximate a near instantaneous curve
    
    if arc_sector is None:
        if not segment.state.initials: raise AttributeError('turn angle not set')
        arc_sector = 0.0 # aircraft does not turn    

    # dimensionalize time
    v_x         = np.cos(beta)*air_speed # np.cos(beta + arc_sector + start_true_course)*air_speed # Updated to reflect final heading. Original: np.cos(beta)*air_speed
    v_y         = np.sin(beta)*air_speed # np.sin(beta + arc_sector + start_true_course)*air_speed # Updated to refelct final heading. Original: np.sin(beta)*air_speed
    t_initial   = conditions.frames.inertial.time[0,0]
    omega       = v_x / radius
    t_final     = arc_sector /omega + t_initial  # (np.abs(arc_sector) *np.pi /180) * radius / air_speed + t_initial # updated
    t_nondim    = segment.state.numerics.dimensionless.control_points
    time        = t_nondim * (t_final-t_initial) + t_initial
    
    # pack
    '''Is this at the end of the the segment?'''
    segment.state.conditions.freestream.altitude[:,0]             = alt
    segment.state.conditions.frames.inertial.position_vector[:,2] = -alt # z points down
    segment.state.conditions.frames.inertial.velocity_vector[:,0] = v_x
    segment.state.conditions.frames.inertial.velocity_vector[:,1] = v_y
    segment.state.conditions.frames.inertial.time[:,0]            = time[:,0]