## @ingroup Library-Methods-Mission-Segments-Common-Initialize
# RCAIDE/Library/Methods/Missions/Segments/Common/Initialize/inertial_position.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Initialize Inertial Position
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Mission-Segments-Common-Initialize
def inertial_position(segment): 
    """ Initializes intertial positon of vehicle
    
        Assumptions:  
            Only used if there is an initial condition
            
        Inputs: 
            state.conditions:           
                numerics.dimensionless.integrate        [i]
                numerics.dimensionless.control_points   [-]
                frames.inertial.aircraft_range          [m]
                inertial.velocity_vector                [m/s]
            
        Outputs: 
            state.conditions.frames.inertial.position_vector  [m]
            state.conditions.frames.inertial.aircraft_range   [m]
           
        Properties Used:
        N/A 
    """      
    if segment.state.initials:
        r_initial = segment.state.initials.conditions.frames.inertial.position_vector
        r_current = segment.state.conditions.frames.inertial.position_vector
        R_initial = segment.state.initials.conditions.frames.inertial.aircraft_range
        R_current = segment.state.conditions.frames.inertial.aircraft_range
        
        if 'altitude' in segment.keys() and segment.altitude is not None:
            r_initial[-1,None,-1] = -segment.altitude
        elif 'altitude_start' in segment.keys() and segment.altitude_start is not None:
            r_initial[-1,None,-1] = -segment.altitude_start
        else:
            assert('Altitude not set')
            
        segment.state.conditions.frames.inertial.position_vector[:,:] = r_current + (r_initial[-1,None,:] - r_current[0,None,:])
        segment.state.conditions.frames.inertial.aircraft_range[:,:]  = R_current + (R_initial[-1,None,:] - R_current[0,None,:])
        
    return 


def _inertial_position(State, Settings, System):
	'''
	Framework version of inertial_position.
	Wraps inertial_position with State, Settings, System pack/unpack.
	Please see inertial_position documentation for more details.
	'''

	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = inertial_position('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System