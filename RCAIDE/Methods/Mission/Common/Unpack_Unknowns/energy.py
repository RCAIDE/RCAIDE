## @ingroup Methods-Missions-Common-Unpack_Unknowns
# RCAIDE/Methods/Missions/Common/Unpack_Unknowns/energy.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  Unpack Unknowns
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Missions-Common-Unpack_Unknowns
def fuel_line_unknowns(segment,fuel_lines):
    flight_controls = segment.flight_controls
    state           = segment.state
    for fuel_line in fuel_lines:
        fuel_line_results   = state.conditions.energy[fuel_line.tag]
        if 'throttle' in segment:
            for propulsor in fuel_line.propulsors:
                fuel_line_results[propulsor.tag].throttle = segment.throttle 
        elif flight_controls.throttle.active:
            num_throttles      = len(flight_controls.throttle.assigned_propulsors)   
            for i in range(num_throttles):
                for j in range(len(flight_controls.throttle.assigned_propulsors[i])): 
                    propulsor_tag = flight_controls.throttle.assigned_propulsors[i][j]
                    fuel_line_results[propulsor_tag].throttle = state.unknowns["throttle_" + str(i)]    
                
        # Thrust Vector Control
        if flight_controls.thrust_vector_angle.active: 
            num_tv_ctrls = len(flight_controls.thrust_vector_angle.assigned_propulsors) 
            for i in range(num_tv_ctrls):   
                for j in range(len(flight_controls.thrust_vector_angle.assigned_propulsors[i])): 
                    propulsor_tag = flight_controls.thrust_vector_angle.assigned_propulsors[i][j]
                    fuel_line_results[propulsor_tag].y_axis_rotation = state.unknowns["thrust_vector_" + str(i)]      
            
        # Blade Pitch Control
        if flight_controls.blade_pitch_angle.active: 
            num_bpa_ctrls = len(flight_controls.blade_pitch_angle.assigned_propulsors) 
            for i in range(num_bpa_ctrls):   
                for j in range(len(flight_controls.blade_pitch_angle.assigned_propulsors[i])): 
                    propulsor_tag = flight_controls.throttle.assigned_propulsors[i][j]
                    fuel_line_results[propulsor_tag].rotor.pitch_command = state.unknowns["blade_pitch_angle_" + str(i)]       
                                                                                      
        # RPM Control
        if flight_controls.RPM.active: 
            num_rpm_ctrls = len(flight_controls.RPM.assigned_propulsors) 
            for i in range(num_rpm_ctrls):   
                for j in range(len(flight_controls.RPM.assigned_propulsors[i])): 
                    propulsor_tag = flight_controls.RPM.assigned_propulsors[i][j]
                    fuel_line_results[propulsor_tag].engine.rpm = state.unknowns["rpm_" + str(i)]  
    return 

def bus_unknowns(segment,busses): 
    flight_controls = segment.flight_controls
    state           = segment.state
    for bus in busses:
        bus_results   = state.conditions.energy[bus.tag] 
        if 'throttle' in segment:
            for propulsor in bus.propulsors:
                bus_results[propulsor.tag].throttle = segment.throttle 
        elif flight_controls.throttle.active:            
            num_throttles = len(flight_controls.throttle.assigned_propulsors)   
            for i in range(num_throttles):
                for j in range(len(flight_controls.throttle.assigned_propulsors[i])): 
                    propulsor_tag = flight_controls.throttle.assigned_propulsors[i][j]
                    bus_results[propulsor_tag].throttle = state.unknowns["throttle_" + str(i)]  

        # Thrust Vector Control
        if flight_controls.thrust_vector_angle.active: 
            num_tv_ctrls = len(flight_controls.thrust_vector_angle.assigned_propulsors) 
            for i in range(num_tv_ctrls):   
                for j in range(len(flight_controls.thrust_vector_angle.assigned_propulsors[i])): 
                    propulsor_tag = flight_controls.thrust_vector_angle.assigned_propulsors[i][j]
                    bus_results[propulsor_tag].y_axis_rotation = state.unknowns["thrust_vector_" + str(i)]      
            
        # Blade Pitch Control
        if flight_controls.blade_pitch_angle.active: 
            num_bpa_ctrls = len(flight_controls.blade_pitch_angle.assigned_propulsors) 
            for i in range(num_bpa_ctrls):   
                for j in range(len(flight_controls.blade_pitch_angle.assigned_propulsors[i])): 
                    propulsor_tag = flight_controls.throttle.assigned_propulsors[i][j]
                    bus_results[propulsor_tag].rotor.pitch_command = state.unknowns["blade_pitch_angle_" + str(i)]     
    return 
     
 
    
