## @ingroup Library-Methods-Mission-Common-Unpack_Unknowns
# RCAIDE/Library/Methods/Missions/Common/Unpack_Unknowns/energy.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  Unpack Unknowns
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Mission-Common-Unpack_Unknowns
def fuel_line_unknowns(segment,fuel_lines):
    flight_controls = segment.flight_controls
    state           = segment.state 

    # Throttle Control 
    if 'throttle' in segment:
        for fuel_line in fuel_lines:
            for propulsor in fuel_line.propulsors: 
                state.conditions.energy[fuel_line.tag][propulsor.tag].throttle[:,0] = segment.throttle 
    elif flight_controls.throttle.active:                
        for i in range(len(flight_controls.throttle.assigned_propulsors)):
            for j in range(len(flight_controls.throttle.assigned_propulsors[i])): 
                propulsor_tag = flight_controls.throttle.assigned_propulsors[i][j]
                for fuel_line in fuel_lines:
                    if propulsor_tag in fuel_line.propulsors:
                        state.conditions.energy[fuel_line.tag][propulsor_tag].throttle = state.unknowns["throttle_" + str(i)]   
     
    # Thrust Vector Control 
    if flight_controls.thrust_vector_angle.active:                
        for i in range(len(flight_controls.thrust_vector_angle.assigned_propulsors)):
            for j in range(len(flight_controls.thrust_vector_angle.assigned_propulsors[i])): 
                propulsor_tag = flight_controls.thrust_vector_angle.assigned_propulsors[i][j]
                for fuel_line in fuel_lines:
                    if propulsor_tag in fuel_line.propulsors:
                        state.conditions.energy[fuel_line.tag][propulsor_tag].y_axis_rotation = state.unknowns["thrust_vector_" + str(i)]   
                    
    # Thrust Vector Control 
    if flight_controls.blade_pitch_angle.active:                
        for i in range(len(flight_controls.blade_pitch_angle.assigned_propulsors)):
            for j in range(len(flight_controls.blade_pitch_angle.assigned_propulsors[i])): 
                propulsor_tag = flight_controls.blade_pitch_angle.assigned_propulsors[i][j]
                for fuel_line in fuel_lines:
                    if propulsor_tag in fuel_line.propulsors:
                        state.conditions.energy[fuel_line.tag][propulsor_tag].rotor.pitch_command = state.unknowns["blade_pitch_angle_" + str(i)]  
              
    # Thrust Vector Control 
    if flight_controls.RPM.active:                
        for i in range(len(flight_controls.RPM.assigned_propulsors)):
            for j in range(len(flight_controls.RPM.assigned_propulsors[i])): 
                propulsor_tag = flight_controls.RPM.assigned_propulsors[i][j]
                for fuel_line in fuel_lines:
                    if propulsor_tag in fuel_line.propulsors:
                        state.conditions.energy[fuel_line.tag][propulsor_tag].engine.rpm = state.unknowns["rpm_" + str(i)]         
                                                                                       
    return 

def bus_unknowns(segment,busses): 
    flight_controls = segment.flight_controls
    state           = segment.state 

    # Throttle Control 
    if 'throttle' in segment:
        for bus in busses:
            for propulsor in bus.propulsors: 
                state.conditions.energy[bus.tag][propulsor.tag].throttle = segment.throttle 
    elif flight_controls.throttle.active:                
        for i in range(len(flight_controls.throttle.assigned_propulsors)):
            for j in range(len(flight_controls.throttle.assigned_propulsors[i])): 
                propulsor_tag = flight_controls.throttle.assigned_propulsors[i][j]
                for bus in busses:
                    if propulsor_tag in bus.propulsors:
                        state.conditions.energy[bus.tag][propulsor_tag].throttle = state.unknowns["throttle_" + str(i)]   
     
    # Thrust Vector Control 
    if flight_controls.thrust_vector_angle.active:                
        for i in range(len(flight_controls.thrust_vector_angle.assigned_propulsors)):
            for j in range(len(flight_controls.thrust_vector_angle.assigned_propulsors[i])): 
                propulsor_tag = flight_controls.thrust_vector_angle.assigned_propulsors[i][j]
                for bus in busses:
                    if propulsor_tag in bus.propulsors:
                        state.conditions.energy[bus.tag][propulsor_tag].y_axis_rotation = state.unknowns["thrust_vector_" + str(i)]  
                    
    # Thrust Vector Control 
    if flight_controls.blade_pitch_angle.active:                
        for i in range(len(flight_controls.blade_pitch_angle.assigned_propulsors)):
            for j in range(len(flight_controls.blade_pitch_angle.assigned_propulsors[i])): 
                propulsor_tag = flight_controls.blade_pitch_angle.assigned_propulsors[i][j]
                for bus in busses:
                    if propulsor_tag in bus.propulsors:
                        state.conditions.energy[bus.tag][propulsor_tag].rotor.pitch_command = state.unknowns["blade_pitch_angle_" + str(i)]   
    return 
     
 
    



def _fuel_line_unknowns(State, Settings, System):
	'''
	Framework version of fuel_line_unknowns.
	Wraps fuel_line_unknowns with State, Settings, System pack/unpack.
	Please see fuel_line_unknowns documentation for more details.
	'''

	#TODO: segment    = [Replace With State, Settings, or System Attribute]
	#TODO: fuel_lines = [Replace With State, Settings, or System Attribute]

	results = fuel_line_unknowns('segment', 'fuel_lines')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System


def _bus_unknowns(State, Settings, System):
	'''
	Framework version of bus_unknowns.
	Wraps bus_unknowns with State, Settings, System pack/unpack.
	Please see bus_unknowns documentation for more details.
	'''

	#TODO: segment = [Replace With State, Settings, or System Attribute]
	#TODO: busses  = [Replace With State, Settings, or System Attribute]

	results = bus_unknowns('segment', 'busses')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System