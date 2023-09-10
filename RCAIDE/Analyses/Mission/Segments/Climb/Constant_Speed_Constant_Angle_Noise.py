## @ingroup Analyses-Mission-Segments-Climb
# RCAIDE/Analyses/Mission/Segments/Climb/Constant_Speed_Constant_Angle_Noise.py
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
#  Constant_Speed_Constant_Angle_Noise
# ---------------------------------------------------------------------------------------------------------------------- 

## @ingroup Analyses-Mission-Segments-Climb
class Constant_Speed_Constant_Angle_Noise(Unknown_Throttle):
    """ Fixed at a true airspeed the vehicle will climb at a constant angle. This is a specific segment for Noise.
        A vehicle performs a climb in accordance with a certification points for takeoff noise.
        Don't use this segment unless you're planning on post process for noise. It is slower than the normal constant
        speed constand angle segment.
    
        Assumptions:
        The points are linearly spaced rather than chebyshev spaced to give the proper "microphone" locations.
        
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
        initialize              = self.process.initialize
        initialize.expand_state = Methods.Climb.Constant_Speed_Constant_Angle_Noise.expand_state        
        initialize.conditions   = Methods.Climb.Constant_Speed_Constant_Angle_Noise.initialize_conditions
    
        return
       