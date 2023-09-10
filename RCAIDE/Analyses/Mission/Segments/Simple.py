## @ingroup Analyses-Mission-Segments
# RCAIDE/Analyses/Missions/Segments/Simple.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE Imports 
from RCAIDE.Analyses import Process
from RCAIDE.Analyses.Mission.Segments import Segment
from RCAIDE.Analyses.Mission.Segments import Conditions 
from RCAIDE.Methods.Missions import Segments as Methods

# ----------------------------------------------------------------------------------------------------------------------
# Simple
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Analyses-Mission-Segments 
class Simple(Segment):
    """ The Second basic piece of a mission which each segment will expand upon
    
        Assumptions:
        There's a detailed process flow outline in defaults. A mission must be solved in that order.
        
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
        
        
        # --------------------------------------------------------------
        #   State
        # --------------------------------------------------------------
        
        # conditions
        self.state.conditions.update( Conditions.Basic() )
        
        # --------------------------------------------------------------
        #   The Solving Process
        # --------------------------------------------------------------
        
        # --------------------------------------------------------------
        #   Initialize - before iteration
        # --------------------------------------------------------------
        initialize = self.process.initialize
        
        initialize.expand_state            = Methods.expand_state
        initialize.differentials           = Methods.Common.Numerics.initialize_differentials_dimensionless
        initialize.conditions              = None
        
        # --------------------------------------------------------------
        #   Converge - starts iteration
        # --------------------------------------------------------------
        converge = self.process.converge 
        converge.converge_root             = Methods.converge_root

        # --------------------------------------------------------------
        #   Iterate - this is iterated
        # --------------------------------------------------------------
        iterate = self.process.iterate
                
        # Update Initials
        iterate.initials = Process()
        iterate.initials.time              = Methods.Common.Frames.initialize_time
        
        # Unpack Unknowns
        iterate.unknowns = Process()
        iterate.unknowns.mission           = None
        
        # Update Conditions
        iterate.conditions = Process()
        iterate.conditions.differentials   = Methods.Common.Numerics.update_differentials_time
        
        # Solve Residuals
        iterate.residuals = Process()

        # --------------------------------------------------------------
        #   Finalize - after iteration
        # --------------------------------------------------------------
        finalize              = self.process.finalize 
        finalize.post_process = Process()
        
        
        return