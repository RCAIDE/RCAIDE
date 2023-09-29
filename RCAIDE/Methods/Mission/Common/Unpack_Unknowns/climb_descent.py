## @ingroup Methods-Missions-Common-Unknowns
# RCAIDE/Methods/Missions/Common/Unknowns/climb_descent.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  Unpack Unknowns
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Missions-Common-Unknowns
def climb_descent(segment):
    """Unpacks the unknowns set in the mission to be available for the mission.

    Assumptions:
    N/A

    Source:
    N/A

    Inputs:
    segment.state.unknowns.throttle            [Unitless]
    segment.state.unknowns.body_angle          [Radians]

    Outputs:
    segment.state.conditions.energy.throttle            [Unitless]
    segment.state.conditions.frames.body.inertial_rotations [Radians]

    Properties Used:
    N/A
    """        
     
    if 'thottle' in segment.state.unknowns: 
        throttle = segment.state.unknowns.throttle
        segment.state.conditions.energy.throttle[:,0] = throttle[:,0]
    
    theta    = segment.state.unknowns.body_angle 
    segment.state.conditions.frames.body.inertial_rotations[:,1] = theta[:,0]    