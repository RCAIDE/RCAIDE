# RCAIDE/Library/Missions/Common/Pre_Process/stability.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
import RCAIDE 
# ----------------------------------------------------------------------------------------------------------------------
#  stability
# ----------------------------------------------------------------------------------------------------------------------  
def stability(mission):
    """ Runs stability model and build surrogate
    
        Assumptions:
            None
        
        Args:
            None
            
        Returns:
            None  
    """      
    last_tag = None
    for tag,segment in mission.segments.items():        
        if type(segment.analyses.stability) == RCAIDE.Framework.Analyses.Stability.VLM_Perturbation_Method: 
            if last_tag != None: 
                segment.analyses.stability.process.compute.lift.inviscid_wings = mission.segments[last_tag].analyses.stability.process.compute.lift.inviscid_wings  
                if segment.analyses.stability.settings.use_surrogate:
                    segment.analyses.stability.surrogates =  mission.segments[last_tag].analyses.surrogates            
            else:
                stab = segment.analyses.stability
                stab.initialize() 
                last_tag = tag 
    return 