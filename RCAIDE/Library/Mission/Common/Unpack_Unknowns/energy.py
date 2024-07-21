# RCAIDE/Library/Missions/Common/Unpack_Unknowns/energy.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  Unpack Unknowns
# ---------------------------------------------------------------------------------------------------------------------- 
def fuel_line_unknowns(segment,fuel_lines):
    """Assigns the unknowns for an fuel-based energy network to the aircraft each iteration of the mission
       solving process.

        Assumptions:
            None
        
        Args: 
            segment  : flight segment        [-] 
            
        Returns:
            None 
    """        
    assigned_control_variables = segment.assigned_control_variables
    state           = segment.state 

    # Throttle Control 
    if 'throttle' in segment:
        for fuel_line in fuel_lines:
            for propulsor in fuel_line.propulsors: 
                state.conditions.energy[fuel_line.tag][propulsor.tag].throttle[:,0] = segment.throttle 
    elif assigned_control_variables.throttle.active:                
        for i in range(len(assigned_control_variables.throttle.assigned_propulsors)):
            for j in range(len(assigned_control_variables.throttle.assigned_propulsors[i])): 
                propulsor_tag = assigned_control_variables.throttle.assigned_propulsors[i][j]
                for fuel_line in fuel_lines:
                    if propulsor_tag in fuel_line.propulsors:
                        state.conditions.energy[fuel_line.tag][propulsor_tag].throttle = state.unknowns["throttle_" + str(i)]   
     
    # Thrust Vector Control 
    if assigned_control_variables.thrust_vector_angle.active:                
        for i in range(len(assigned_control_variables.thrust_vector_angle.assigned_propulsors)):
            for j in range(len(assigned_control_variables.thrust_vector_angle.assigned_propulsors[i])): 
                propulsor_tag = assigned_control_variables.thrust_vector_angle.assigned_propulsors[i][j]
                for fuel_line in fuel_lines:
                    if propulsor_tag in fuel_line.propulsors:
                        state.conditions.energy[fuel_line.tag][propulsor_tag].y_axis_rotation = state.unknowns["thrust_vector_" + str(i)]      
    return 

def bus_unknowns(segment,busses): 
    """Assigns the unknowns for an electric-based energy network to the aircraft each iteration of the mission
       solving process.

        Assumptions:
            None
        
        Args: 
            segment  : flight segment        [-] 
            
        Returns:
            None 
    """        
    assigned_control_variables = segment.assigned_control_variables
    state           = segment.state 

    # Throttle Control 
    if 'throttle' in segment:
        for bus in busses:
            for propulsor in bus.propulsors: 
                state.conditions.energy[bus.tag][propulsor.tag].throttle[:,0] = segment.throttle 
    elif assigned_control_variables.throttle.active:                
        for i in range(len(assigned_control_variables.throttle.assigned_propulsors)):
            for j in range(len(assigned_control_variables.throttle.assigned_propulsors[i])): 
                propulsor_tag = assigned_control_variables.throttle.assigned_propulsors[i][j]
                for bus in busses:
                    if propulsor_tag in bus.propulsors:
                        state.conditions.energy[bus.tag][propulsor_tag].throttle = state.unknowns["throttle_" + str(i)]   
     
    # Thrust Vector Control 
    if assigned_control_variables.thrust_vector_angle.active:                
        for i in range(len(assigned_control_variables.thrust_vector_angle.assigned_propulsors)):
            for j in range(len(assigned_control_variables.thrust_vector_angle.assigned_propulsors[i])): 
                propulsor_tag = assigned_control_variables.thrust_vector_angle.assigned_propulsors[i][j]
                for bus in busses:
                    if propulsor_tag in bus.propulsors:
                        state.conditions.energy[bus.tag][propulsor_tag].y_axis_rotation = state.unknowns["thrust_vector_" + str(i)]    
    return 
     
 
    
