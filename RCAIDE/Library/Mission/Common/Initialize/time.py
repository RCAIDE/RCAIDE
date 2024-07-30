# RCAIDE/Library/Missions/Common/Initialize/time.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  Initialize Time
# ---------------------------------------------------------------------------------------------------------------------- 
def time(segment):
    """ Sets the initial time of the vehicle at the start of the segment
    
        Assumptions:
            Only used if there is an initial condition 
        
        Args: 
            segment  : flight segment        [-] 
            
        Returns:
            None  
    """        
    
    if segment.state.initials:
        t_initial = segment.state.initials.conditions.frames.inertial.time
        t_current = segment.state.conditions.frames.inertial.time 
        segment.state.conditions.frames.inertial.time[:,:] = t_current + (t_initial[-1,0] - t_current[0,0])
        
    else:
        t_initial = segment.state.conditions.frames.inertial.time[0,0]
        
    if segment.state.initials:
        segment.state.conditions.frames.planet.start_time = segment.state.initials.conditions.frames.planet.start_time
        
    elif 'start_time' in segment:
        segment.state.conditions.frames.planet.start_time = segment.start_time
    
    return 