## @ingroup Methods-Missions-Common-Unknowns
# RCAIDE/Methods/Missions/Common/Unknowns/level_flight.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  Unpack Unknowns
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Missions-Common-Unknowns
def level_flight(segment):
    """ Unpacks the throttle setting and body angle from the solver to the mission
    
        Assumptions:
        N/A
        
        Inputs:
            state.unknowns:
                throttle    [Unitless]
                body_angle  [Radians]
            
        Outputs:
            state.conditions:
                propulsion.throttle            [Unitless]
                frames.body.inertial_rotations [Radians]

        Properties Used:
        N/A
                                
    """    
     
    if 'throttle' in segment.state.unknowns: 
        throttle = segment.state.unknowns.throttle
        segment.state.conditions.energy.throttle[:,0] = throttle[:,0]
         
    body_angle = segment.state.unknowns.body_angle 
    segment.state.conditions.frames.body.inertial_rotations[:,1] = body_angle[:,0]   
     
 
    
