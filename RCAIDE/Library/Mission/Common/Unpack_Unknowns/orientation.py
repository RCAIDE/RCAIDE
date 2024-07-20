## @ingroup Library-Missions-Common-Unpack_Unknowns
# RCAIDE/Library/Missions/Common/Unpack_Unknowns/orientation.py
# 
# 
# Created:  Jul 2023, M. Clarke
# ----------------------------------------------------------------------------------------------------------------------
#  Unpack Unknowns
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Missions-Common-Unpack_Unknowns
def orientation(segment): 
        
    # Body Angle Control
    if segment.assigned_control_variables.body_angle.active:  
        segment.state.conditions.frames.body.inertial_rotations[:,1] = segment.state.unknowns.body_angle[:,0]

    if segment.assigned_control_variables.bank_angle.active: 
        segment.state.conditions.frames.body.inertial_rotations[:,0] = segment.state.unknowns.bank_angle[:,0]
    
    # Velocity Control
    if segment.assigned_control_variables.velocity.active:
        segment.state.conditions.frames.inertial.velocity_vector[:,0] = segment.state.unknowns.velocity[:,0]
        
    # Altitude Control
    if segment.assigned_control_variables.altitude.active:
        segment.state.conditions.frames.inertial.position_vector[:,2] = -segment.state.unknowns.altitude[:,0]
        
    return 
            
            
            