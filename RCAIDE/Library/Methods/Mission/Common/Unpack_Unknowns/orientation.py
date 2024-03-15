## @ingroup Library-Methods-Mission-Common-Unpack_Unknowns
# RCAIDE/Library/Methods/Missions/Common/Unpack_Unknowns/orientation.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  Unpack Unknowns
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Mission-Common-Unpack_Unknowns
def orientation(segment): 
        
    # Body Angle Control
    if segment.flight_controls.body_angle.active:  
        segment.state.conditions.frames.body.inertial_rotations[:,1] = segment.state.unknowns.body_angle[:,0]      
    
    # Velocity Control
    if segment.flight_controls.velocity.active:
        segment.state.conditions.frames.inertial.velocity_vector[:,0] = segment.state.unknowns.velocity[:,0]
        
    # Altitude Control
    if segment.flight_controls.altitude.active:
        segment.state.conditions.frames.inertial.position_vector[:,2] = -segment.state.unknowns.altitude[:,0]
        
    return 
            
            
            


def _orientation(State, Settings, System):
	'''
	Framework version of orientation.
	Wraps orientation with State, Settings, System pack/unpack.
	Please see orientation documentation for more details.
	'''

	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = orientation('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System