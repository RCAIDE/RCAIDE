## @ingroup Analyses-Functions-Segments-Climb
# Constant_Mach_Constant_Rate.py
#
# Created:  
# Modified: Feb 2016, Andrew Wendorff

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# SUAVE imports
from Legacy.trunk.S.Methods.Missions import Segments as Methods

from .Unknown_Throttle import Unknown_Throttle

# Units
from Legacy.trunk.S.Core import Units


# ----------------------------------------------------------------------
#  Segment
# ----------------------------------------------------------------------

## @ingroup Analyses-Functions-Segments-Climb
class Constant_Mach_Constant_Rate(Unknown_Throttle):
    """ Climb at a constant mach number and at a constant rate.
    
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
        
        # --------------------------------------------------------------
        #   User inputs
        # --------------------------------------------------------------
        self.altitude_start = None # Optional
        self.altitude_end   = 10. * Units.km
        self.climb_rate     = 3.  * Units.m / Units.s
        self.mach_number    = 0.7 
        self.true_course    = 0.0 * Units.degrees        
        
        # --------------------------------------------------------------
        #   The Solving Process
        # --------------------------------------------------------------
    
        # only need to change one setup step from constant_speed_constant_rate
        initialize = self.process.initialize
        initialize.conditions = Methods.Climb.Constant_Mach_Constant_Rate.initialize_conditions

        

        return

