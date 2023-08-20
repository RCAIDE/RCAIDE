# RCAIDE/Methods/Missions/Segments/Common/Noise.py
# (c) Copyright The Board of Trustees of RCAIDE
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