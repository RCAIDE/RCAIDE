# RCAIDE/Library/Missions/Segments/Common/Initialize/inertial_position.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  Initialize Inertial Position
# ----------------------------------------------------------------------------------------------------------------------
def inertial_position(segment): 
    """ Initializes intertial positon of vehicle
    
        Assumptions:  
            Only used if there is an initial condition
        
        Args: 
            segment  : flight segment        [-] 
            
        Returns:
            None 
    """      
    if segment.state.initials:
        r_initial = segment.state.initials.conditions.frames.inertial.position_vector
        r_current = segment.state.conditions.frames.inertial.position_vector
        R_initial = segment.state.initials.conditions.frames.inertial.aircraft_range
        R_current = segment.state.conditions.frames.inertial.aircraft_range
        
        if 'altitude' in segment.keys() and segment.altitude is not None:
            r_initial[-1,None,-1] = -segment.altitude
        elif 'altitude_start' in segment.keys() and segment.altitude_start is not None:
            r_initial[-1,None,-1] = -segment.altitude_start
        else:
            assert('Altitude not set')
            
        segment.state.conditions.frames.inertial.position_vector[:,:] = r_current + (r_initial[-1,None,:] - r_current[0,None,:])
        segment.state.conditions.frames.inertial.aircraft_range[:,:]  = R_current + (R_initial[-1,None,:] - R_current[0,None,:])
        
    return 