## @ingroup Methods-Missions-Common-Update
# RCAIDE/Methods/Missions/Common/Update/stability.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Stability
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Missions-Common-Update
def stability(segment): 
    """ Updates the stability of the aircraft 
        
        Assumptions:
        N/A
        
        Inputs:
            None 
                 
        Outputs: 
            None
      
        Properties Used:
        N/A
                    
    """   
    # unpack
    conditions = segment.state.conditions
    stability_model = segment.analyses.stability
    
    # call aerodynamics model
    if stability_model:
        results = stability_model( segment.state.conditions )
        conditions.stability.update(results)
    
    return