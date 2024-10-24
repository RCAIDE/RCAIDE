# RCAIDE/Library/Missions/Common/Pre_Process/stability.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team
# Modified:

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
    for idx,tag_segment in enumerate(mission.segments.items()):     
        tag, segment = tag_segment
        
        if (type(segment.analyses.stability) == RCAIDE.Framework.Analyses.Stability.Vortex_Lattice_Method): # This check will need to be updated later
            if idx==0:
                stab = segment.analyses.stability
                stab.initialize() 
                if (type(segment.analyses.aerodynamics) == RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method):
                    segment.analyses.stability.process.compute.lift.inviscid_wings = segment.analyses.aerodynamics.process.compute.lift.inviscid_wings 
                last_tag = tag                 
                continue
            
            if (type(segment.analyses.stability) == RCAIDE.Framework.Analyses.Stability.Vortex_Lattice_Method):
                if last_tag and  'compute' in mission.segments[last_tag].analyses.stability.process: 
                    segment.analyses.stability.process.compute.lift.inviscid_wings = mission.segments[last_tag].analyses.stability.process.compute.lift.inviscid_wings  
                

    return 