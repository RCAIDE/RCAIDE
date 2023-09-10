## @ingroup Methods-Missions-Segments-Common
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  Update Noise
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Missions-Segments-Common
def compute_noise(segment):
    """ Evaluates the energy network to find the thrust force and mass rate

        Inputs -
            segment.analyses.noise             [Function]

        Outputs
            N/A

        Assumptions - None  
    """    
    noise_model = segment.analyses.noise
    
    if noise_model:
        noise_model.evaluate_noise(segment)    