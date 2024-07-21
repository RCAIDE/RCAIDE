# RCAIDE/Library/Missions/Common/Unpack_Unknowns/orientation.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  Unpack Unknowns
# ---------------------------------------------------------------------------------------------------------------------- 
def orientation(segment): 
    """Assigns the unknowns for the aircraft orientation to the aircraft each iteration of
       the mission solving process.

        Assumptions:
            None
        
        Args: 
            segment  : flight segment        [-] 
            
        Returns:
            None 
    """        
        
    # Body Angle Control (effectively angle of attack)
    if segment.assigned_control_variables.body_angle.active:  
        segment.state.conditions.frames.body.inertial_rotations[:,1] = segment.state.unknowns.body_angle[:,0]

    # Bank Angle Control
    if segment.assigned_control_variables.bank_angle.active: 
        segment.state.conditions.frames.body.inertial_rotations[:,0] = segment.state.unknowns.bank_angle[:,0]
    
    # Velocity Control
    if segment.assigned_control_variables.velocity.active:
        segment.state.conditions.frames.inertial.velocity_vector[:,0] = segment.state.unknowns.velocity[:,0]
        
    # Altitude Control
    if segment.assigned_control_variables.altitude.active:
        segment.state.conditions.frames.inertial.position_vector[:,2] = -segment.state.unknowns.altitude[:,0]
        
    return 
            
            
            