## @ingroup Library-Methods-Missions-Segments-Common-Pre_Process
# RCAIDE/Library/Methods/Missions/Common/Pre_Process/stability.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
import RCAIDE 
# ----------------------------------------------------------------------------------------------------------------------
#  stability
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Methods-Missions-Segments-Common-Pre_Process
def stability(mission):
    """ Runs stability model and build surrogate
    
        Assumptions:
            N/A
        
        Inputs:
            None
            
        Outputs:
            None 

        Properties Used:
        N/A                
    """      
    last_tag = None
    for tag,segment in mission.segments.items():        
        if type(segment.analyses.stability) == RCAIDE.Framework.Analyses.Stability.VLM_Perturbation_Method: 
            if last_tag: 
                segment.analyses.stability.process.compute.lift.inviscid_wings = mission.segments[last_tag].analyses.stability.process.compute.lift.inviscid_wings  
            else:
                stab = segment.analyses.stability 
                stab.process.compute.lift.inviscid_wings.geometry                = stab.geometry 
                stab.process.compute.lift.inviscid_wings.settings.model_fuselage = stab.settings.model_fuselage
                stab.process.compute.lift.inviscid_wings.initialize()    
                last_tag = tag  
    return 