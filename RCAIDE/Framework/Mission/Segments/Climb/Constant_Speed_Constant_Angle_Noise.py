## @ingroup Framework-Mission-Segments-Climb
# RCAIDE/Framework/Mission/Segments/Climb/Constant_Speed_Constant_Angle_Noise.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Core                           import Units 
from RCAIDE.Framework.Mission.Segments.Evaluate      import Evaluate
from RCAIDE.Library.Mission                          import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Speed_Constant_Angle_Noise
# ---------------------------------------------------------------------------------------------------------------------- 

## @ingroup Framework-Mission-Segments-Climb
class Constant_Speed_Constant_Angle_Noise(Evaluate):
    """ Fixed at a true airspeed the vehicle will climb at a constant angle. This is a specific segment for Noise.
        A vehicle performs a climb in accordance with a certification points for takeoff noise.
        Don't use this segment unless you're planning on post process for noise. It is slower than the normal constant
        speed constand angle segment. 
    """       
    
    def __defaults__(self):
        """ This sets the default solver flow. Anything in here can be modified after initializing a segment.
    
            Assumptions:
                None
    
            Source:
                self : mission segment [-]
    
            Args:
                None
    
            Returns:
                None
        """          
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude_start    = None # Optional
        self.altitude_end      = 10. * Units.km
        self.climb_angle       = 3.  * Units.deg
        self.air_speed         = 100 * Units.m / Units.s
        self.true_course_angle = 0.0 * Units.degrees            
                
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------   
        initialize                         = self.process.initialize  
        initialize.expand_state            = Segments.Climb.Constant_Speed_Constant_Angle_Noise.expand_state
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = Segments.Climb.Constant_Speed_Constant_Angle_Noise.initialize_conditions  
        iterate                            = self.process.iterate
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation   
        
        return
       