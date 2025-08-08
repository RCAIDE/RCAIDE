# RCAIDE/Library/Missions/Common/Update/stability.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  Stability
# ---------------------------------------------------------------------------------------------------------------------- 
def stability(segment): 
    """ Updates the stability of the aircraft 
        
        Assumptions:
        If stability model is defined, overwrite the aerodynamics calculations
        
        Inputs:
            None 
                 
        Outputs: 
            None
      
        Properties Used:
        N/A
                    
    """   
    # unpack
    stability_model    = segment.analyses.stability 
        
    if stability_model != None: 
        _ = stability_model(segment)

    return