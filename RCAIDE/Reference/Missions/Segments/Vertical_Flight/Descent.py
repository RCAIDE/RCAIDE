# RCAIDE/Framework/Functions/Segments/Vertical_Flight/Descent.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Reference.Core import Units
from RCAIDE.Framework.Missions.Mission import Evaluate
from RCAIDE.Reference.Missions.Functions import Common


# ----------------------------------------------------------------------------------------------------------------------
#  Descent
# ----------------------------------------------------------------------------------------------------------------------
class Descent(Evaluate):
    """ A vertically descending hover for VTOL aircraft.
    """      
    
    def __defaults__(self):
        """ Specific flight segment defaults which can be modified after initializing.
        
            Assumptions:
                None
    
            Source:
                None
        """               
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        
        self.altitude_start    = None # Optional
        self.altitude_end      = 1. * Units.km
        self.descent_rate      = 1.  * Units.m / Units.s
        self.true_course       = 0.0 * Units.degrees  
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Functions specific processes
        # --------------------------------------------------------------------------------------------------------------  
        initialize                         = self.process.initialize
        iterate                            = self.process.iterate 
        initialize.conditions              = RCAIDE.Framework.Mission.Mission.Segments.Vertical_Flight.Descent.initialize_conditions
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        return
       