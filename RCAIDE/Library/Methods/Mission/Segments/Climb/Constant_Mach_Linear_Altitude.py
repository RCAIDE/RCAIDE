## @ingroup Library-Methods-Mission-Segments-Climb
# RCAIDE/Library/Methods/Missions/Segments/Climb/Constant_Mach_Linear_Altitude.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE  
from RCAIDE.Library.Methods.Mission.Common.Update  import atmosphere

# Package imports  
import numpy as np
 
# ----------------------------------------------------------------------------------------------------------------------
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Mission-Segments-Climb
def initialize_conditions(segment):
    """Sets the specified conditions which are given for the segment type.

    Assumptions:
    Constrant dynamic pressure and constant rate of climb

    Source:
    N/A

    Inputs:
    segment.mach_number                         [unitless]
    segment.dynamic_pressure                    [pascals]
    segment.altitude_start                      [meters]
    segment.altitude_end                        [meters]
    segment.distance                            [meters]

    Outputs:
    conditions.frames.inertial.velocity_vector  [meters/second]
    conditions.frames.inertial.position_vector  [meters]
    conditions.freestream.altitude              [meters]
    conditions.frames.inertial.time             [seconds]

    Properties Used:
    N/A
    """        
    
    # unpack
    alt0       = segment.altitude_start 
    altf       = segment.altitude_end
    xf         = segment.distance
    mach       = segment.mach_number
    conditions = segment.state.conditions  
    t_nondim   = segment.state.numerics.dimensionless.control_points
    
    # check for initial altitude
    if alt0 is None:
        if not segment.state.initials: raise AttributeError('altitude not set')
        alt0 = -1.0 * segment.state.initials.conditions.frames.inertial.position_vector[-1,2]
        
    # discretize on altitude
    alt = t_nondim * (altf-alt0) + alt0      
    segment.state.conditions.freestream.altitude[:,0] = alt[:,0]

    # check for initial velocity
    if mach is None: 
        if not segment.state.initials: raise AttributeError('mach not set')
        air_speed = np.linalg.norm(segment.state.initials.conditions.frames.inertial.velocity_vector[-1])   
    else:
        
        # Update freestream to get speed of sound
        atmosphere(segment)
        a          = conditions.freestream.speed_of_sound    
    
        # compute speed, constant with constant altitude
        air_speed    = mach * a   
        
    climb_angle  = np.arctan((altf-alt0)/xf)
    v_x          = np.cos(climb_angle)*air_speed
    v_z          = np.sin(climb_angle)*air_speed 
    t_nondim     = segment.state.numerics.dimensionless.control_points
    
    # discretize on altitude
    alt = t_nondim * (altf-alt0) + alt0    
    
    # pack
    conditions.freestream.altitude[:,0]             = alt[:,0]
    conditions.frames.inertial.position_vector[:,2] = -alt[:,0] # z points down 
    conditions.frames.inertial.velocity_vector[:,0] = v_x[:,0]
    conditions.frames.inertial.velocity_vector[:,2] = -v_z[:,0]      


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