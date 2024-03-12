## @ingroup Frameworks-Mission-Segments-Transition
# RCAIDE/Frameworks/Mission/Segments/Transition/Constant_Acceleration_Constant_Angle_Linear_Climb.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Core                                     import Units 
from RCAIDE.Frameworks.Mission.Segments.Evaluate       import Evaluate
from RCAIDE.Methods.Mission                          import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Acceleration_Constant_Angle_Linear_Climb
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Frameworks-Mission-Segments-Transition
class Constant_Acceleration_Constant_Angle_Linear_Climb(Evaluate):
    """ Vehicle accelerates at a constant rate between two airspeeds.
    
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
        #   User Inputs
        # --------------------------------------------------------------
        self.altitude_start         = None
        self.altitude_end           = None
        self.air_speed_start        = None
        self.climb_angle            = 0.0 * Units['rad'] 
        self.acceleration           = 1.  * Units['m/s/s'] 
        self.pitch_initial          = None
        self.pitch_final            = 0.0 * Units['rad']
        self.true_course_angle      = 0.0 * Units.degrees  
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------  
        initialize                         = self.process.initialize 
        initialize.conditions              = Segments.Transition.Constant_Acceleration_Constant_Angle_Linear_Climb.initialize_conditions  
        iterate                            = self.process.iterate  
        iterate.residuals.total_forces     = Common.Residuals.level_flight_forces 
        
        return

