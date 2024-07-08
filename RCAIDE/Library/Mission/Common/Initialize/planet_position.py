# RCAIDE/Library/Missions/Segments/Common/Initialize/Frames.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Initialize Planet Position
# ----------------------------------------------------------------------------------------------------------------------
def planet_position(segment):
    """ Sets the initial location of the vehicle relative to the planet at the start of the segment
    
        Assumptions:
            Only used if there is an initial condition
         
        Args: 
            segment  : flight segment        [-] 
            
        Returns:
            None
    """        
    
    if segment.state.initials:
        longitude_initial = segment.state.initials.conditions.frames.planet.longitude[-1,0]
        latitude_initial  = segment.state.initials.conditions.frames.planet.latitude[-1,0] 
    elif 'latitude' in segment:
        longitude_initial = segment.longitude
        latitude_initial  = segment.latitude      
    else:
        longitude_initial = 0.0
        latitude_initial  = 0.0

    segment.state.conditions.frames.planet.longitude[:,0] = longitude_initial
    segment.state.conditions.frames.planet.latitude[:,0]  = latitude_initial    

    return 