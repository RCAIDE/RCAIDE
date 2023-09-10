## @ingroup Analyses-Mission-Segments-Climb
# RCAIDE/Analyses/Mission/Segments/Climb/Constant_Speed_Constant_Angle.py
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
#  Constant_Speed_Constant_Angle
# ---------------------------------------------------------------------------------------------------------------------- 

## @ingroup Analyses-Mission-Segments-Climb
class Constant_Speed_Constant_Angle(Unknown_Throttle):
    """ A basic constant true airspeed climb at a constant angle. Usually used for certification to ensure a vehicle
        can clear and obstacle.
    
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
        self.climb_angle       = 3.  * Units.deg
        self.air_speed         = 100 * Units.m / Units.s
        self.true_course_angle = 0.0 * Units.degrees    
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   SOLVING PROCESS
        # --------------------------------------------------------------------------------------------------------------  
        initialize            = self.process.initialize
        initialize.conditions = Methods.Climb.Constant_Speed_Constant_Angle.initialize_conditions
    
        return
       