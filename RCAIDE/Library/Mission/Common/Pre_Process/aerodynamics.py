# RCAIDE/Library/Missions/Common/Pre_Process/aerodynamics.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
import RCAIDE 
# ----------------------------------------------------------------------------------------------------------------------
#  aerodynamics
# ----------------------------------------------------------------------------------------------------------------------  
def aerodynamics(mission):
    """ Runs aerdoynamics model and build surrogate
    
        Assumptions:
            None
        
        Args:
            None
            
        Returns:
            None  
    """      
    last_tag = None
    for tag,segment in mission.segments.items():        
        if (type(segment.analyses.aerodynamics) == RCAIDE.Framework.Analyses.Aerodynamics.Subsonic_VLM) or (type(segment.analyses.aerodynamics) == RCAIDE.Framework.Analyses.Aerodynamics.Supersonic_VLM): 
            if last_tag != None:
                segment.analyses.aerodynamics.process.compute.lift.inviscid_wings = mission.segments[last_tag].analyses.aerodynamics.process.compute.lift.inviscid_wings 
                if segment.analyses.aerodynamics.settings.use_surrogate:
                    segment.analyses.aerodynamics.surrogates =  mission.segments[last_tag].analyses.aerodynamics.surrogates
            else:
                if type(segment.analyses.stability) == RCAIDE.Framework.Analyses.Stability.VLM_Perturbation_Method:
                    segment.analyses.aerodynamics.process.compute.lift.inviscid_wings = segment.analyses.stability.process.compute.lift.inviscid_wings
                    segment.analyses.aerodynamics.surrogates =  segment.analyses.stability.surrogates
                else:
                    aero   = segment.analyses.aerodynamics
                    aero.initialize()   
        last_tag = tag  
    return 