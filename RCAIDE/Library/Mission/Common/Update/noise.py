# RCAIDE/Library/Missions/Common/Update/noise.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  noise
# ---------------------------------------------------------------------------------------------------------------------- 
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