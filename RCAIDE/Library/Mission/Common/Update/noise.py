## @ingroup Library-Missions-Segments-Common-Update
# RCAIDE/Library/Missions/Common/Update/noise.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  noise
# ----------------------------------------------------------------------------------------------------------------------

## @ingroup Library-Missions-Segments-Common-Update
def noise(segment):
    """ Computes the noise using the prescribed method 
        
        Assumptions:
            None
            
        Source:
            None
            
        Args:
            None
                 
        Returns: 
            None      
    """   
    noise_model = segment.analyses.noise
    
    if noise_model:
        noise_model.evaluate(segment)    