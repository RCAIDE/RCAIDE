## @ingroup Framework-Mission-Segments-Transition
# RCAIDE/Framework/Mission/Segments/Transition/Constant_Acceleration_Constant_Pitchrate_Constant_Altitude.py 
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Core                            import Units 
from RCAIDE.Framework.Mission.Segments.Evaluate       import Evaluate
from RCAIDE.Library.Mission                           import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Acceleration_Constant_Pitchrate_Constant_Altitude
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Framework-Mission-Segments-Transition
class Constant_Acceleration_Constant_Pitchrate_Constant_Altitude(Evaluate):
    """ Vehicle accelerates at a constant rate between two airspeeds. 
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
        
        # --------------------------------------------------------------
        #   User Inputs
        # --------------------------------------------------------------
        self.altitude           = None
        self.acceleration       = 1.  * Units['m/s/s']
        self.air_speed_start    = None
        self.air_speed_end      = 1.0 * Units['m/s']        
        self.pitch_initial      = None
        self.pitch_final        = 0.0 * Units['rad']
        self.true_course_angle  = 0.0 * Units.degrees   
         
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------          
        initialize                         = self.process.initialize 
        initialize.conditions              = Segments.Transition.Constant_Acceleration_Constant_Pitchrate_Constant_Altitude.initialize_conditions      
        iterate                            = self.process.iterate    
        iterate.residuals.flight_dynamics  = Common.Residuals.level_flight_dynamics
        
        return