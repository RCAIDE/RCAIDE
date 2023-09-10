## @ingroup Analyses-Mission-Segments-Climb
# RCAIDE/Analyses/Mission/Segments/Climb/Constant_Mach_Linear_Altitude.py
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
# Constant_Mach_Linear_Altitude
# ---------------------------------------------------------------------------------------------------------------------- 

## @ingroup Analyses-Mission-Segments-Climb
class Constant_Mach_Linear_Altitude(Unknown_Throttle):
    """ Climb at a constant mach number but linearly change altitudes over a distance.
    
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
        self.mach              = 0.5
        self.distance          = 10. * Units.km
        self.altitude_start    = None
        self.altitude_end      = None
        self.true_course_angle = 0.0 * Units.degrees    
        
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   SOLVING PROCESS
        # --------------------------------------------------------------------------------------------------------------  
        initialize            = self.process.initialize
        initialize.conditions = Methods.Climb.Constant_Mach_Linear_Altitude.initialize_conditions 

        return

