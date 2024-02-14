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
    if segment.flight_controls.throttle.active:
        for fuel_line in fuel_lines:
            fuel_line_results   = segment.state.conditions.energy[fuel_line.tag]    
            num_throttles      = len(segment.flight_controls.throttle.assigned_propulsors)   
            for i in range(num_throttles):
                for j in range(len(segment.flight_controls.throttle.assigned_propulsors[i])): 
                    propulsor_name = segment.flight_controls.throttle.assigned_propulsors[i][j]
                    fuel_line_results[propulsor_name].throttle = segment.state.unknowns["throttle_" + str(i)]     
    
    return 

def bus_unknowns(segment,busses): 
    if segment.flight_controls.throttle.active:
        for bus in busses:
            bus_results   = segment.state.conditions.energy[bus.tag]    
            num_throttles      = len(segment.flight_controls.throttle.assigned_propulsors)   
            for i in range(num_throttles):
                for j in range(len(segment.flight_controls.throttle.assigned_propulsors[i])): 
                    propulsor_name = segment.flight_controls.throttle.assigned_propulsors[i][j]
                    bus_results[propulsor_name].throttle = segment.state.unknowns["throttle_" + str(i)] 
                    

    # Thrust Vector Control
    if segment.thrust_vector_angle_control.active: 
        num_tv_ctrls = len(segment.thrust_vector_angle_control.assigned_propulsors) 
        for i in range(num_tv_ctrls):   
            segment.state.unknowns["thrust_control_" + str(i)]      
        
    # Blade Pitch Control
    if segment.blade_pitch_angle_control.active: 
        num_bpa_ctrls = len(segment.blade_pitch_angle_control.assigned_propulsors) 
        for i in range(num_bpa_ctrls):   
            segment.state.unknowns["blade_pitch_angle_" + str(i)]       
                                                                                  
    # RPM Control
    if segment.RPM_control.active: 
        num_rpm_ctrls = len(segment.RPM_control.assigned_propulsors) 
        for i in range(num_rpm_ctrls):   
            segment.state.unknowns["rpm_control_" + str(i)]  
    
    return 
     
 
    
