## @ingroup Library-Methods-Mission-Segments-Common-Pre_Process
# RCAIDE/Library/Methods/Missions/Common/Pre_Process/flight_dynamics_and_controls.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
from RCAIDE.Frameworks.Core import Units

# ----------------------------------------------------------------------------------------------------------------------
#  flight_dynamics_and_controls
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Methods-Mission-Segments-Common-Pre_Process
def flight_dynamics_and_controls(mission):
    """ Sets the flight dynamics residuals and fligth controls of the aircraft   

        Assumptions:
        N/A

        Inputs: 
            mission     - data structure of mission  [-]
 
        Outputs:  

        Properties Used:
        N/A

    """     
    for segment in mission.segments:  
        ones_row    = segment.state.ones_row 
        ctrls       = segment.flight_controls
        dynamics    = segment.flight_dynamics
        
        # assign force and moment residuals i.e. degrees of freedom 
        num_DOF  = 0      
        if dynamics.force_x == True: 
            segment.state.residuals.force_x = ones_row(1) *0 
            num_DOF += 1 
        if dynamics.force_y == True:
            segment.state.residuals.force_y = ones_row(1) *0
            num_DOF += 1  
        if dynamics.force_z == True:
            segment.state.residuals.force_z = ones_row(1) *0
            num_DOF += 1  
        if dynamics.moment_x == True:
            segment.state.residuals.moment_x = ones_row(1) *0
            num_DOF += 1  
        if dynamics.moment_y == True:
            segment.state.residuals.moment_y = ones_row(1) *0 
            num_DOF += 1 
        if dynamics.moment_z == True:
            segment.state.residuals.moment_z = ones_row(1) *0
            num_DOF += 1  
        
        # assign control variables   
        ones_row     = segment.state.ones_row 
        num_ctrls    = 0
        
        # Body Angle  
        if ctrls.body_angle.active:
            if ctrls.body_angle.initial_guess:
                segment.state.unknowns.body_angle = ones_row(1) * ctrls.body_angle.initial_guess_values[0][0]
            else:
                segment.state.unknowns.body_angle = ones_row(1) * 3.0 * Units.degrees 
            num_ctrls += 1    
                
        # Wing Angle  
        if ctrls.wind_angle.active:
            if ctrls.wind_angle.initial_guess:
                segment.state.unknowns.wind_angle = ones_row(1) * ctrls.wind_angle.initial_guess_values[0][0]
            else:
                segment.state.unknowns.wind_angle = ones_row(1) * 1.0 * Units.degrees 
            num_ctrls += 1            
            
        # Throttle 
        if ctrls.throttle.active: 
            for i in range(len(ctrls.throttle.assigned_propulsors)): 
                if ctrls.throttle.initial_guess: 
                    for j in range(len(ctrls.throttle.assigned_propulsors[i])):   
                        segment.state.unknowns["throttle_" + str(i)] = ones_row(1) * ctrls.throttle.initial_guess_values[i][j] 
                else:
                    segment.state.unknowns["throttle_" + str(i)] = ones_row(1) *  0.5
                num_ctrls += 1    
        
        # Velocity 
        if ctrls.velocity.active:  
            if ctrls.velocity.initial_guess:
                segment.state.unknowns.velocity = ones_row(1) * ctrls.velocity.initial_guess_values[0][0] 
            else:
                segment.state.unknowns.velocity = ones_row(1) *  100
            num_ctrls += 1    
                        
                
        # Acceleration 
        if ctrls.acceleration.active:  
            if ctrls.acceleration.initial_guess:
                segment.state.unknowns.acceleration = ones_row(1) * ctrls.acceleration.initial_guess_values[0][0] 
            else:
                segment.state.unknowns.acceleration = ones_row(1) *  1.
            num_ctrls += 1   

        # Time
        if ctrls.elapsed_time.active:  
            if ctrls.elapsed_time.initial_guess:    
                segment.state.unknowns.elapsed_time = ctrls.elapsed_time.initial_guess_values[0][0] 
            else:
                segment.state.unknowns.elapsed_time = 10
            num_ctrls += 1                         
                                
        # Elevator 
        if ctrls.elevator_deflection.active:     
            for i in range(len(ctrls.elevator_deflection.assigned_surfaces)): 
                if ctrls.elevator_deflection.initial_guess:  
                    for j in range(len(ctrls.elevator_deflection.assigned_surfaces[i])): 
                        segment.state.unknowns["elevator_" + str(i)] = ones_row(1) * ctrls.elevator_deflection.initial_guess_values[i][j]
                else:
                    segment.state.unknowns["elevator_" + str(i)] = ones_row(1) * 0.0 * Units.degrees  
                num_ctrls += 1   
                    
        # Flap  
        if ctrls.flap_deflection.active:  
            for i in range(len(ctrls.flap_deflection.assigned_surfaces)):
                if ctrls.flap_deflection.initial_guess:       
                    for j in range(len(ctrls.flap_deflection.assigned_surfaces[i])):
                        segment.state.unknowns["flap_" + str(i)] = ones_row(1) * ctrls.flap_deflection.initial_guess_values[i][j]
                else:
                    segment.state.unknowns["flap_" + str(i)] = ones_row(1) * 0.0 * Units.degrees 
                num_ctrls += 1    
        # Slat  
        if ctrls.slat_deflection.active:  
            for i in range(len(ctrls.slat_deflection.assigned_surfaces)):  
                if ctrls.slat_deflection.initial_guess:     
                    for j in range(len(ctrls.slat_deflection.assigned_surfaces[i])):
                        segment.state.unknowns["slat_" + str(i)] = ones_row(1) * ctrls.slat_deflection.initial_guess_values[i][j]
                else:
                    segment.state.unknowns["slat_" + str(i)] = ones_row(1) * 0.0 * Units.degrees 
                num_ctrls += 1   
                
        # Aileron  
        if ctrls.aileron_deflection.active:  
            for i in range(len(ctrls.aileron_deflection.assigned_surfaces)):   
                if ctrls.aileron_deflection.initial_guess:    
                    for j in range(len(ctrls.aileron_deflection.assigned_surfaces[i])): 
                        segment.state.unknowns["aileron_" + str(i)] = ones_row(1) * ctrls.aileron_deflection.initial_guess_values[i][j] 
                else: 
                    segment.state.unknowns["aileron_" + str(i)] = ones_row(1) * 0.0 * Units.degrees 
                num_ctrls += 1       
            
        # Thrust 
        if ctrls.thrust_vector_angle.active:  
            for i in range(len(ctrls.thrust_vector_angle.assigned_propulsors)):  
                if ctrls.thrust_vector_angle.initial_guess:     
                    for j in range(len(ctrls.thrust_vector_angle.assigned_surfaces[i])): 
                        segment.state.unknowns["thrust_vector_" + str(i)] = ones_row(1) * ctrls.thrust_vector_angle.initial_guess_values[i][j]
                else:
                    segment.state.unknowns["thrust_vector_" + str(i)] = ones_row(1) * 0.0 * Units.degrees 
                num_ctrls += 1       
            
        # Blade Pitch 
        if ctrls.blade_pitch_angle.active:  
            for i in range(len(ctrls.blade_pitch_angle.assigned_propulsors)):   
                if ctrls.blade_pitch_angle.initial_guess:    
                    for j in range(len(ctrls.blade_pitch_angle.assigned_propulsors[i])):   
                        segment.state.unknowns["blade_pitch_angle_" + str(i)] = ones_row(1) * ctrls.blade_pitch_angle.initial_guess_values[i][j]
                else:
                    segment.state.unknowns["blade_pitch_angle_" + str(i)] = ones_row(1) * 0.0 * Units.degrees 
                num_ctrls += 1      
                                                                                      
        # RPM  
        if ctrls.RPM.active:  
            for i in range(len(ctrls.RPM.assigned_propulsors)):   
                if ctrls.RPM.initial_guess:    
                    for j in range(len(ctrls.RPM.assigned_propulsors[i])):
                        segment.state.unknowns["rpm_" + str(i)] = ones_row(1) * ctrls.RPM.initial_guess_values[i][j]
                else:
                    segment.state.unknowns["rpm_" + str(i)] = ones_row(1) * 2400 
                num_ctrls += 1
                
                
        # if the degrees of freedom are greater than the number of control inputs, post problem at optimization  # TO DO
                                                                                                                                                                