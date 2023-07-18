## @ingroup Analyses-Mission 
# RCAIDE/Analyses/Mission/Sequential_Segments.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# legacy imports 
from   Legacy.trunk.S.Methods import Missions as Methods

# RCAIDE imports 
from .Mission import Mission

# ----------------------------------------------------------------------------------------------------------------------
# Sequential_Segments
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Analyses-Mission
class Sequential_Segments(Mission):
    """ Solves each segment one at time
    
        Assumptions:
        None
        
        Source:
        None
    """
    
    def __defaults__(self):
        """This sets the default values.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            None
    
            Outputs:
            None
    
            Properties Used:
            None
        """          
        
        self.tag = 'mission'
        
        
        # --------------------------------------------------------------
        #   THE SOLVING PROCESS
        # --------------------------------------------------------------
        
        # --------------------------------------------------------------
        #   Initialize
        # --------------------------------------------------------------
        self.process.initialize = Methods.Segments.Common.Sub_Segments.expand_sub_segments

        # --------------------------------------------------------------
        #   Converge
        # --------------------------------------------------------------
        self.process.converge = Methods.Segments.Common.Sub_Segments.sequential_sub_segments
        
        # --------------------------------------------------------------
        #   Iterate
        # --------------------------------------------------------------        
        del self.process.iterate


        return