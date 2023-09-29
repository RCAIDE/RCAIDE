## @ingroup Methods-Missions-Common-Update
# RCAIDE/Methods/Missions/Common/Update/stability.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Stability
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Missions-Common-Update
def stability(segment): 
    """  
    """    

    # unpack
    conditions = segment.state.conditions
    stability_model = segment.analyses.stability
    
    # call aerodynamics model
    if stability_model:
        results = stability_model( segment.state.conditions )
        conditions.stability.update(results)
    
    return