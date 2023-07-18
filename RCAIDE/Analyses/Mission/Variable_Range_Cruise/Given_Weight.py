## @ingroup Analyses-Mission-Variable_Range_Cruise  
# RCAIDE/Analyses/Mission/Variable_Range_Cruise/Given_Weight.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from RCAIDE.Methods          import Missions as Methods
from RCAIDE.Analyses.Mission import All_At_Once

# ----------------------------------------------------------------------------------------------------------------------
# Given_Weight
# ---------------------------------------------------------------------------------------------------------------------- 

## @ingroup Analyses-Mission-Vary_Cruise
class Given_Weight(All_At_Once):
    """ Given a target landing weight, select the cruise distance by adding a residual to the mission
    
        Assumptions:
        None
        
        Source:
        None
    """
    
    def __defaults__(self):
        """This sets the default flow of methods for the mission.
    
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
        
        self.tag = 'vary_cruise_given_weight'
        
        # --------------------------------------------------------------------------------------------------------------
        #   USER INPUTS
        # --------------------------------------------------------------------------------------------------------------
        self.cruise_tag            = 'cruise'
        self.target_landing_weight = 1000.0
        
        
        # --------------------------------------------------------------------------------------------------------------
        #   STATE
        # --------------------------------------------------------------------------------------------------------------
        
        # initials and unknowns, on top of segment initials and unknowns
        self.state.unknowns.cruise_distance  = 1000.0
        self.state.residuals.landing_weight  = 0.0 
        

        # --------------------------------------------------------------------------------------------------------------
        #   THE SOLVING PROCESS
        # --------------------------------------------------------------------------------------------------------------
    
        # --------------------------------------------------------------------------------------------------------------
        #   INITALIZE (BEFORE INTERATION)
        # --------------------------------------------------------------------------------------------------------------
        self.process.initialize.expand_state        = Methods.Segments.expand_state
        self.process.initialize.expand_sub_segments = Methods.Segments.Common.Sub_Segments.expand_sub_segments
        self.process.initialize.cruise_distance     = Methods.Segments.Cruise.Variable_Cruise_Distance.initialize_cruise_distance
        
        # --------------------------------------------------------------------------------------------------------------
        #  CONVERGE (STARTS INTERATION)
        # --------------------------------------------------------------------------------------------------------------
        self.process.converge.converge_root         = Methods.Segments.converge_root
        
        # --------------------------------------------------------------------------------------------------------------
        #  ITERATE
        # --------------------------------------------------------------------------------------------------------------
        iterate = self.process.iterate  
        iterate.clear()
        
        # unpack the unknown
        iterate.unpack_distance              = Methods.Segments.Cruise.Variable_Cruise_Distance.unknown_cruise_distance
        
        # Run the Segments
        iterate.unpack                       = Methods.Segments.Common.Sub_Segments.unpack_subsegments
        iterate.sub_segments                 = Methods.Segments.Common.Sub_Segments.update_sub_segments
        iterate.merge_sub_segment_states     = Methods.Segments.Common.Sub_Segments.merge_sub_segment_states
        
        # Solve Residuals
        self.process.iterate.residual_weight = Methods.Segments.Cruise.Variable_Cruise_Distance.residual_landing_weight
        
        
        # --------------------------------------------------------------
        #  FINALIZE
        # --------------------------------------------------------------        
        self.process.finalize.sub_segments   = Methods.Segments.Common.Sub_Segments.finalize_sub_segments
        