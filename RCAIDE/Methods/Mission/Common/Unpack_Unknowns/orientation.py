## @ingroup Methods-Missions-Common-Unpack_Unknowns
# RCAIDE/Methods/Missions/Common/Unpack_Unknowns/orientation.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  Unpack Unknowns
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Missions-Common-Unpack_Unknowns
def orientation(segment): 
        
    # Body Angle Control
    if segment.flight_controls.body_angle.active:  
        segment.state.conditions.frames.body.inertial_rotations[:,1] = segment.state.unknowns.body_angle[:,0]      
    
    # Velocity Control
    if segment.flight_controls.velocity.active:
        segment.state.conditions.frames.inertial.velocity_vector[:,0] = segment.state.unknowns.velocity[:,0]
        
    # Altitude Control
    if segment.flight_controls.altitudes.active:
        segment.state.conditions.frames.inertial.position_vector[:,2] = -segment.state.unknowns.altitudes[:,0]
        
    return 
            
            
            