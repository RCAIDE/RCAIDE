# RCAIDE/Library/Missions/Common/Update/altitude.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Update Altitude
# ---------------------------------------------------------------------------------------------------------------------- 
def altitude(segment):
    """ Updates freestream altitude from inertial position. Computes the following variables: 
            segment.state.conditions.freestream.altitude             [meters] 
        
        Assumptions:
        None
        
        Args:
            segment.state.conditions.frames.inertial.position_vector [meters]
            
        Returns:
            None
    """    
    altitude = -segment.state.conditions.frames.inertial.position_vector[:,2]
    segment.state.conditions.freestream.altitude[:,0] = altitude 