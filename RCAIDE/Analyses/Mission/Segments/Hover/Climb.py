## @ingroup Analyses-Mission-Segments-Hover
# RCAIDE/Analyses/Mission/Segments/Hover/Climb.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Methods.Missions import Segments as Methods  
from .Hover                  import Hover 
from RCAIDE.Core             import Units

# ----------------------------------------------------------------------------------------------------------------------
#  Climb
# ----------------------------------------------------------------------------------------------------------------------

## @ingroup Analyses-Mission-Segments-Hover
class Climb(Hover):
    """ A vertically climbing hover for VTOL aircraft. Although the vehicle moves, no aerodynamic drag and lift are used.
    
        Assumptions:
        Your vehicle creates a negligible drag and lift force during a vertical climb.
        
        Source:
        None
    """     
    
    def __defaults__(self):
        """ This sets the default solver flow. Anything in here can be modified after initializing a segment.
    
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
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   USER INPUTS
        # -------------------------------------------------------------------------------------------------------------- 
        
        self.altitude_start    = None # Optional
        self.altitude_end      = 1. * Units.km
        self.climb_rate        = 1.  * Units.m / Units.s
        self.true_course_angle = 0.0 * Units.degrees 
        
        # --------------------------------------------------------------
        #   THE SOLVING PROCESS
        # --------------------------------------------------------------
        initialize = self.process.initialize
        iterate    = self.process.iterate
        
        initialize.conditions = Methods.Hover.Climb.initialize_conditions
    
        return
       