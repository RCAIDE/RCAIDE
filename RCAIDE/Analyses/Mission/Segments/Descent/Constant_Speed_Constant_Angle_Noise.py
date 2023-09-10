## @ingroup Analyses-Mission-Segments-Descent
# RCAIDE/Analyses/Mission/Segments/Descent/Constant_Speed_Constant_Angle_Noise.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports
import RCAIDE 
from RCAIDE.Methods.Missions                                 import Segments as Methods 
from RCAIDE.Analyses.Mission.Segments.Climb.Unknown_Throttle import Unknown_Throttle 
from RCAIDE.Core                                             import Units

# ----------------------------------------------------------------------------------------------------------------------  
#  Constant_Speed_Constant_Angle_Noise
# ----------------------------------------------------------------------------------------------------------------------   

## @ingroup Analyses-Mission-Segments-Descent
class Constant_Speed_Constant_Angle_Noise(Unknown_Throttle):
    """ Fixed at a true airspeed the vehicle will descend at a constant angle. This is a specific segment for Noise.
        A vehicle performs a descent to landing in accordance with a certification points for landing noise.
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
        self.altitude_end      = 0.0 * Units.km
        self.descent_angle     = 3.  * Units.deg
        self.air_speed         = 100 * Units.m / Units.s
        self.true_course_angle = 0.0 * Units.degrees 
        
        self.state.numerics.discretization_method = RCAIDE.Methods.Utilities.Chebyshev.linear_data
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   SOLVING PROCESS
        # -------------------------------------------------------------------------------------------------------------- 
        initialize              = self.process.initialize
        initialize.conditions   = Methods.Descent.Constant_Speed_Constant_Angle_Noise.initialize_conditions
        initialize.expand_state = Methods.Descent.Constant_Speed_Constant_Angle_Noise.expand_state
        
        return

