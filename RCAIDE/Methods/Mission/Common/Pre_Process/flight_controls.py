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
def flight_controls(mission):
    """ Sets the flight controls of the aircraft depending on the number of degrees of freedom
        and the type of segment 

        Assumptions:
        N/A

        Inputs: 
            mission     - data structure of mission  [-]
 
        Outputs:  

        Properties Used:
        N/A

    """     
    for segment in mission.segments:    
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
            for i in range(len(segment.throttle_control.assigned_propulsors)):   
                segment.state.unknowns["throttle_" + str(i)] = ones_row(1) * segment.throttle_control.initial_values[i][0] 
                number_of_control_variables += 1
            if number_of_control_variables > degrees_of_freedom:
                assert('Number of control variables on aircraft is greated than the specified degrees of freedom')         
                     
        # Elevator Control
        if segment.elevator_deflection_control.active:  
            for i in range(len(segment.elevator_deflection_control.assigned_propulsors)):   
                segment.state.unknowns["elevator_control_" + str(i)] = ones_row(1) * segment.elevator_deflection_control.initial_values[i][0]
                number_of_control_variables += 1
            if number_of_control_variables > degrees_of_freedom:
                assert('Number of control variables on aircraft is greated than the specified degrees of freedom')    
                    
        # Flap Control
        if segment.flap_deflection_control.active:  
            for i in range(len(segment.flap_deflection_control.assigned_propulsors)):   
                segment.state.unknowns["flap_control_" + str(i)] = ones_row(1) * segment.flap_deflection_control.initial_values[i][0]
                number_of_control_variables += 1
            if number_of_control_variables > degrees_of_freedom:
                assert('Number of control variables on aircraft is greated than the specified degrees of freedom')      
                
        # Aileron Control
        if segment.aileron_deflection_control.active:  
            for i in range(len(segment.aileron_deflection_control.assigned_propulsors)):   
                segment.state.unknowns["aileron_control_" + str(i)] = ones_row(1) * segment.aileron_deflection_control.initial_values[i][0]  
                number_of_control_variables += 1
            if number_of_control_variables > degrees_of_freedom:
                assert('Number of control variables on aircraft is greated than the specified degrees of freedom')       
            
        # Thrust Control
        if segment.thrust_vector_angle_control.active:  
            for i in range(len(segment.aileron_deflection_control.assigned_propulsors)):   
                segment.state.unknowns["thrust_control_" + str(i)] = ones_row(1) * segment.thrust_vector_angle_control.initial_values[i][0]
                number_of_control_variables += 1
            if number_of_control_variables > degrees_of_freedom:
                assert('Number of control variables on aircraft is greated than the specified degrees of freedom')       
            
        # Blade Pitch Control
        if segment.blade_pitch_angle_control.active:  
            for i in range(segment.blade_pitch_angle_control.assigned_propulsors):   
                segment.state.unknowns["blade_pitch_angle_" + str(i)] = ones_row(1) * segment.blade_pitch_angle_control.initial_values[i][0]
                number_of_control_variables += 1
            if number_of_control_variables > degrees_of_freedom:
                assert('Number of control variables on aircraft is greated than the specified degrees of freedom')       
                                                                                      
        # RPM Control
        if segment.RPM_control.active:  
            for i in range(len(segment.RPM_control.assigned_propulsors) ):   
                segment.state.unknowns["rpm_control_" + str(i)] = ones_row(1) * segment.RPM_control.initial_values[i][0]
                number_of_control_variables += 1
            if number_of_control_variables > degrees_of_freedom:
                assert('Number of control variables on aircraft is greated than the specified degrees of freedom')       
                                                                                                                                                                