## @ingroup Library-Methods-Mission-Segments-Single_Point
# RCAIDE/Library/Methods/Missions/Segments/Single_Point/Set_Speed_Set_Throttle.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 
 
# ----------------------------------------------------------------------------------------------------------------------  
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------  

import numpy as np

# ----------------------------------------------------------------------------------------------------------------------  
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Methods-Mission-Segments-Single_Point
def initialize_conditions(segment):
    """Sets the specified conditions which are given for the segment type.

    Assumptions:
    A fixed speed and throttle

    Source:
    N/A

    Inputs:
    segment.altitude                               [meters]
    segment.air_speed                              [meters/second]
    segment.throttle                               [unitless]
    segment.acceleration_z                         [meters/second^2]
    segment.state.unknowns.acceleration            [meters/second^2]

    Outputs:
    conditions.frames.inertial.acceleration_vector [meters/second^2]
    conditions.frames.inertial.velocity_vector     [meters/second]
    conditions.frames.inertial.position_vector     [meters]
    conditions.freestream.altitude                 [meters]
    conditions.frames.inertial.time                [seconds]

    Properties Used:
    N/A
    """      
    
    # unpack
    alt              = segment.altitude
    air_speed        = segment.air_speed 
    acceleration_z   = segment.acceleration_z
    acceleration     = segment.state.unknowns.acceleration  
    
    # check for initial altitude
    if alt is None:
        if not segment.state.initials: raise AttributeError('altitude not set')
        alt = -1.0 *segment.state.initials.conditions.frames.inertial.position_vector[-1,2]
    
    # pack
    segment.state.conditions.freestream.altitude[:,0]             = alt
    segment.state.conditions.frames.inertial.position_vector[:,2] = -alt # z points down
    segment.state.conditions.frames.inertial.velocity_vector[:,0] = air_speed
    segment.state.conditions.frames.inertial.acceleration_vector  = np.array([[acceleration,0.0,acceleration_z]]) 
    
# ----------------------------------------------------------------------------------------------------------------------  
#  Unpack Unknowns 
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Methods-Mission-Segments-Single_Point
def unpack_unknowns(segment):
    """ Unpacks the x accleration and body angle from the solver to the mission
    
        Assumptions:
        N/A
        
        Inputs:
            segment.state.unknowns:
                acceleration                        [meters/second^2]
                body_angle                          [radians]
            
        Outputs:
            segment.state.conditions:
                frames.inertial.acceleration_vector [meters/second^2]
                frames.body.inertial_rotations      [radians]

        Properties Used:
        N/A
                                
    """      
    
    # unpack unknowns
    acceleration  = segment.state.unknowns.acceleration
    body_angle    = segment.state.unknowns.body_angle
    
    # apply unknowns
    segment.state.conditions.frames.inertial.acceleration_vector[0,0] = acceleration
    segment.state.conditions.frames.body.inertial_rotations[:,1]      = body_angle[:,0]      


def _initialize_conditions(State, Settings, System):
	'''
	Framework version of initialize_conditions.
	Wraps initialize_conditions with State, Settings, System pack/unpack.
	Please see initialize_conditions documentation for more details.
	'''

	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = initialize_conditions('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System


def _unpack_unknowns(State, Settings, System):
	'''
	Framework version of unpack_unknowns.
	Wraps unpack_unknowns with State, Settings, System pack/unpack.
	Please see unpack_unknowns documentation for more details.
	'''

	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = unpack_unknowns('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System