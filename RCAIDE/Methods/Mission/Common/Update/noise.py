## @ingroup Methods-Missions-Segments-Common-Update
# RCAIDE/Methods/Missions/Common/Update/noise.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  compute_noise
# ----------------------------------------------------------------------------------------------------------------------

## @ingroup Methods-Missions-Segments-Common-Update
def noise(segment):
    """  

    """    
    noise_model = segment.analyses.noise
    
    if noise_model:
        noise_model.evaluate_noise(segment)    