## @ingroup Library-Methods-Mission-Common-Update  
# RCAIDE/Library/Methods/Missions/Common/Update/altitude.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Update Altitude
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Mission-Common-Update 
def altitude(segment):
    """ Updates freestream altitude from inertial position
        
        Assumptions:
        N/A
        
        Inputs:
            segment.state.conditions:
                frames.inertial.position_vector [meters]
        Outputs:
            segment.state.conditions:
                freestream.altitude             [meters]
      
        Properties Used:
        N/A
                    
    """    
    altitude = -segment.state.conditions.frames.inertial.position_vector[:,2]
    segment.state.conditions.freestream.altitude[:,0] = altitude 