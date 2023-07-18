## @ingroup Analyses-Mission
# RCAIDE/Analyses/Mission/All_At_Once.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  

# RCAIDE Imports
from .Mission import Mission 
from RCAIDE.Methods import Missions as Methods

# ----------------------------------------------------------------------------------------------------------------------
# All_At_Once
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Analyses-Mission
class All_At_Once(Mission):
    """ Solves all segments and sub segments at once
    
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
        #   Initialize
        # --------------------------------------------------------------
        self.process.initialize.expand_state             = Methods.Segments.expand_state
        self.process.initialize.expand_sub_segments      = Methods.Segments.Common.Sub_Segments.expand_sub_segments
        self.process.initialize.merge_sub_segment_states = Methods.Segments.Common.Sub_Segments.merge_sub_segment_states

        # --------------------------------------------------------------
        #   Converge
        # --------------------------------------------------------------
        self.process.converge.converge_root         = Methods.Segments.converge_root
        
        # --------------------------------------------------------------
        #   Iterate
        # --------------------------------------------------------------        
        self.process.iterate.unpack                   = Methods.Segments.Common.Sub_Segments.unpack_subsegments
        self.process.iterate.sub_segments             = Methods.Segments.Common.Sub_Segments.update_sub_segments
        self.process.iterate.merge_sub_segment_states = Methods.Segments.Common.Sub_Segments.merge_sub_segment_states
