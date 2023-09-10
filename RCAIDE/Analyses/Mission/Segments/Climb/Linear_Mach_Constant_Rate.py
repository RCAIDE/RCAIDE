## @ingroup Analyses-Mission-Segments-Climb
# RCAIDE/Analyses/Mission/Segments/Climb/Linear_Mach_Constant_Rate.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Core             import Units
from RCAIDE.Methods.Missions import Segments as Methods 
from .Unknown_Throttle       import Unknown_Throttle

# ----------------------------------------------------------------------------------------------------------------------
#  Linear_Mach_Constant_Rate
# ---------------------------------------------------------------------------------------------------------------------- 

## @ingroup Analyses-Mission-Segments-Climb
class Linear_Mach_Constant_Rate(Unknown_Throttle):
    """ Linearly change mach number while climbing at a constant rate.
    
        Assumptions:
        None
        
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
        self.altitude_end      = 10. * Units.km
        self.climb_rate        = 3.  * Units.m / Units.s
        self.mach_number_end   = 0.7
        self.mach_number_start = 0.8
        self.true_course_angle = 0.0 * Units.degrees    
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   SOLVING PROCESS
        # --------------------------------------------------------------------------------------------------------------  
        initialize            = self.process.initialize
        initialize.conditions = Methods.Climb.Linear_Mach_Constant_Rate.initialize_conditions 
        return

