## @ingroup Library-Methods-Mission-Segments-Hover
# RCAIDE/Library/Methods/Missions/Segments/Hover/Descent.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 
 
# ----------------------------------------------------------------------------------------------------------------------  
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------  

## @ingroup Library-Methods-Mission-Segments-Hover
def initialize_conditions(segment):
    """Sets the specified conditions which are given for the segment type.

    Assumptions:
    Descent segment with a constant rate.

    Source:
    N/A

    Inputs:
    segment.altitude_start                              [meters]
    segment.altitude_end                                [meters]
    segment.descent_rate                                [meters/second]
    segment.state.numerics.dimensionless.control_points [Unitless]
    segment.state.conditions.frames.inertial.time       [seconds]

    Outputs:
    conditions.frames.inertial.velocity_vector  [meters/second]
    conditions.frames.inertial.position_vector  [meters]
    conditions.freestream.altitude              [meters]
    conditions.frames.inertial.time             [seconds]

    Properties Used:
    N/A
    """      
    
    # unpack
    descent_rate = segment.descent_rate
    alt0         = segment.altitude_start 
    altf         = segment.altitude_end
    t_nondim     = segment.state.numerics.dimensionless.control_points
    t_initial    = segment.state.conditions.frames.inertial.time[0,0]
    conditions   = segment.state.conditions  

    # check for initial altitude
    if alt0 is None:
        if not segment.state.initials: raise AttributeError('initial altitude not set')
        alt0 = -1.0 *segment.state.initials.conditions.frames.inertial.position_vector[-1,2]

    # discretize on altitude
    alt = t_nondim * (altf-alt0) + alt0
    
    # process velocity vector
    v_z = descent_rate # z points down    
    dt  = (alt0 - altf)/descent_rate

    # rescale operators
    t = t_nondim * dt

    # pack
    t_initial = segment.state.conditions.frames.inertial.time[0,0]
    segment.state.conditions.frames.inertial.time[:,0] = t_initial + t[:,0]    
    
    # pack conditions    
    conditions.frames.inertial.velocity_vector[:,0] = 0.
    conditions.frames.inertial.velocity_vector[:,2] = v_z
    conditions.frames.inertial.position_vector[:,2] = -alt[:,0] # z points down
    conditions.freestream.altitude[:,0]             =  alt[:,0] # positive altitude in this context
    conditions.frames.inertial.time[:,0]            = t_initial + t[:,0]


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