## @ingroup Library-Missions-Common-Unpack_Unknowns
# RCAIDE/Library/Missions/Common/Unpack_Unknowns/energy.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  Unpack Unknowns
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Missions-Common-Unpack_Unknowns
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
            propulsor_tags = flight_controls.throttle.assigned_propulsors[i]
            for j in range(len(propulsor_tags)): 
                for fuel_line in fuel_lines:
                    if propulsor_tags[j] in fuel_line.propulsors:
                        state.conditions.energy[fuel_line.tag][propulsor_tags[j]].throttle = state.unknowns["throttle_" + str(i)]   
     
    # Thrust Vector Control 
    if flight_controls.thrust_vector_angle.active:                
        for i in range(len(flight_controls.thrust_vector_angle.assigned_propulsors)): 
            propulsor_tags = flight_controls.throttle.assigned_propulsors[i]
            for j in range(len(propulsor_tags)): 
                for fuel_line in fuel_lines:
                    if propulsor_tags[j] in fuel_line.propulsors:
                        state.conditions.energy[fuel_line.tag][propulsor_tags[j]].y_axis_rotation = state.unknowns["thrust_vector_" + str(i)]    
    return 

def bus_unknowns(segment,busses): 
    flight_controls = segment.flight_controls
    state           = segment.state 

    # Throttle Control 
    if 'throttle' in segment:
        for bus in busses:
            for propulsor in bus.propulsors: 
                state.conditions.energy[bus.tag][propulsor.tag].throttle[:,0] = segment.throttle 
    elif flight_controls.throttle.active:                
        for i in range(len(flight_controls.throttle.assigned_propulsors)): 
            propulsor_tags = flight_controls.throttle.assigned_propulsors[i]
            for j in range(len(propulsor_tags)): 
                for bus in busses:
                    if propulsor_tags[j] in bus.propulsors:
                        state.conditions.energy[bus.tag][propulsor_tags[j]].throttle = state.unknowns["throttle_" + str(i)]  
     
    # Thrust Vector Control 
    if flight_controls.thrust_vector_angle.active:                
        for i in range(len(flight_controls.thrust_vector_angle.assigned_propulsors)): 
            propulsor_tags = flight_controls.throttle.assigned_propulsors[i]
            for j in range(len(propulsor_tags)): 
                for bus in busses:
                    if propulsor_tags[j] in bus.propulsors:
                        state.conditions.energy[bus.tag][propulsor_tags[j]].y_axis_rotation = state.unknowns["thrust_vector_" + str(i)]
    return 
     
 
    
