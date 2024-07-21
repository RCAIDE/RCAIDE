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
        if (type(segment.analyses.aerodynamics) == RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method):
            if last_tag and  'compute' in mission.segments[last_tag].analyses.aerodynamics.process: 
                segment.analyses.aerodynamics.process.compute.lift.inviscid_wings = mission.segments[last_tag].analyses.aerodynamics.process.compute.lift.inviscid_wings
                segment.analyses.aerodynamics.surrogates       = mission.segments[last_tag].analyses.aerodynamics.surrogates 
                segment.analyses.aerodynamics.reference_values = mission.segments[last_tag].analyses.aerodynamics.reference_values 
                
            else:          
                aero   = segment.analyses.aerodynamics
                aero.initialize()   
                last_tag = tag
    return 