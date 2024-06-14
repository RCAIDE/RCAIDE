## @ingroup Library-Missions-Common-Update
# RCAIDE/Library/Missions/Common/Update/gravity.py
# 
# 
# Created:  Jul 2023, M. Clarke


# ----------------------------------------------------------------------------------------------------------------------
#  Update Gravity
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Missions-Common-Update
def gravity(segment):
    """ Sets the gravity for each part of the mission
    
        Assumptions:
        Fixed sea level gravity, doesn't use a gravity model yet
        
        Inputs:
        segment.analyses.planet.features.sea_level_gravity [Data] 
            
        Outputs:
        state.conditions.freestream.gravity [meters/second^2]

        Properties Used:
        N/A
                                
    """      

    # unpack
    planet = segment.analyses.planet
    H      = segment.conditions.freestream.altitude
    
    # calculate
    g      = planet.features.compute_gravity(H)

    # pack
    segment.state.conditions.freestream.gravity[:,0] = g[:,0]

    return 