# RCAIDE/Library/Missions/Common/Pre_Process/aerodynamics.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke
# Modified: Jul 2024, E. Botero

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
            A change has been made that requires the aero model to be initialized
        
        Args:
            None
            
        Returns:
            None  
    """      
    
    
    for idx,tag_segment in enumerate(mission.segments.items()):    
        tag, segment = tag_segment
        # Run the aerodynamics surrogate fresh everytime we run a mission
        if idx==0:
            aero   = segment.analyses.aerodynamics
            aero.initialize()   
            last_tag = tag     
            continue
            
        
        if (type(segment.analyses.aerodynamics) == RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method):
            if last_tag and  'compute' in mission.segments[last_tag].analyses.aerodynamics.process: 
                segment.analyses.aerodynamics.process.compute.lift.inviscid_wings = mission.segments[last_tag].analyses.aerodynamics.process.compute.lift.inviscid_wings
                segment.analyses.aerodynamics.surrogates       = mission.segments[last_tag].analyses.aerodynamics.surrogates 
                segment.analyses.aerodynamics.reference_values = mission.segments[last_tag].analyses.aerodynamics.reference_values 
        else:
            raise('Aerodynamics Model Not Supported Yet')                
    return 