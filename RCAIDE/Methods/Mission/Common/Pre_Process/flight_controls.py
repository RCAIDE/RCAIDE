## @ingroup Methods-Missions-Segments-Common-Pre_Process
# RCAIDE/Methods/Missions/Common/Pre_Process/flight_controls.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
#  flight_controls
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Methods-Missions-Segments-Common-Pre_Process
def flight_controls(segment):
    """ Sets the flight controls of the aircraft depending on the number of degrees of freedom
        and the type of segment 

        Assumptions:
        N/A

        Inputs: 
 
        Outputs:  

        Properties Used:
        N/A

    """    
    degrees_of_freedom             = segment.degrees_of_freedom
    ones_row                       = segment.state.ones_row 
    number_of_control_variables    = 0    
    segment.state.residuals.forces = ones_row(degrees_of_freedom) * 0.0
    
    # Body Angle Control
    if segment.body_angle_control.active:
        segment.state.unknowns.body_angle = ones_row(1) * segment.body_angle_control.initial_values[0][0] 
        number_of_control_variables += 1
        if number_of_control_variables > degrees_of_freedom:
            assert('Number of control variables on aircraft is greated than the specified degrees of freedom')
            
    # Wing Angle Control
    if segment.wind_angle_control.active:
        segment.state.unknowns.wind_angle = ones_row(1) * segment.wind_angle_control.initial_values[0][0] 
        number_of_control_variables += 1
        if number_of_control_variables > degrees_of_freedom:
            assert('Number of control variables on aircraft is greated than the specified degrees of freedom')            
        
    # Throttle Control
    if segment.throttle_control.active:
        num_throttle_ctrls = len(segment.throttle_control.assigned_propulsors) 
        for i in range(num_throttle_ctrls):   
            segment.state.unknowns["throttle_" + str(i)] = ones_row(1) * segment.throttle_control.initial_values[0][i] 
            number_of_control_variables += 1
        if number_of_control_variables > degrees_of_freedom:
            assert('Number of control variables on aircraft is greated than the specified degrees of freedom')         
                 
    # Elevator Control
    if segment.elevator_deflection_control.active: 
        num_elev_ctrls = len(segment.throttle_control.assigned_propulsors) 
        for i in range(num_elev_ctrls):   
            segment.state.unknowns["elevator_control_" + str(i)] = ones_row(1) * segment.elevator_deflection_control.initial_values[0][i]
            number_of_control_variables += 1
        if number_of_control_variables > degrees_of_freedom:
            assert('Number of control variables on aircraft is greated than the specified degrees of freedom')    
                
    # Flap Control
    if segment.flap_deflection_control.active: 
        num_flap_ctrls = len(segment.throttle_control.assigned_propulsors) 
        for i in range(num_flap_ctrls):   
            segment.state.unknowns["flap_control_" + str(i)] = ones_row(1) * segment.flap_deflection_control.initial_values[0][i]
            number_of_control_variables += 1
        if number_of_control_variables > degrees_of_freedom:
            assert('Number of control variables on aircraft is greated than the specified degrees of freedom')      
            
    # Aileron Control
    if segment.aileron_deflection_control.active: 
        num_aile_ctrls = len(segment.throttle_control.assigned_propulsors) 
        for i in range(num_aile_ctrls):   
            segment.state.unknowns["aileron_control_" + str(i)] = ones_row(1) * segment.aileron_deflection_control.initial_values[0][i]
            number_of_control_variables += 1
        if number_of_control_variables > degrees_of_freedom:
            assert('Number of control variables on aircraft is greated than the specified degrees of freedom')       
        
    # Thrust Control
    if segment.thrust_vector_angle_control.active: 
        num_tv_ctrls = len(segment.throttle_control.assigned_propulsors) 
        for i in range(num_tv_ctrls):   
            segment.state.unknowns["thrust_control_" + str(i)] = ones_row(1) * segment.thrust_vector_angle_control.initial_values[0][i]
            number_of_control_variables += 1
        if number_of_control_variables > degrees_of_freedom:
            assert('Number of control variables on aircraft is greated than the specified degrees of freedom')       
        
    # Blade Pitch Control
    if segment.blade_pitch_angle_control.active: 
        num_bpa_ctrls = len(segment.throttle_control.assigned_propulsors) 
        for i in range(num_bpa_ctrls):   
            segment.state.unknowns["blade_pitch_angle_" + str(i)] = ones_row(1) * segment.blade_pitch_angle_control.initial_values[0][i]
            number_of_control_variables += 1
        if number_of_control_variables > degrees_of_freedom:
            assert('Number of control variables on aircraft is greated than the specified degrees of freedom')       
                                                                                  
    # RPM Control
    if segment.RPM_control.active: 
        num_rpm_ctrls = len(segment.throttle_control.assigned_propulsors) 
        for i in range(num_rpm_ctrls):   
            segment.state.unknowns["rpm_control_" + str(i)] = ones_row(1) * segment.RPM_control.initial_values[0][i]
            number_of_control_variables += 1
        if number_of_control_variables > degrees_of_freedom:
            assert('Number of control variables on aircraft is greated than the specified degrees of freedom')       
                                                                                                                                                                