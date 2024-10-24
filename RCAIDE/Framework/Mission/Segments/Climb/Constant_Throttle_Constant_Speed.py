# RCAIDE/Framework/Functions/Segments/Climb/Constant_Throttle_Constant_Speed.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Core                           import Units 
from RCAIDE.Framework.Mission.Segments.Evaluate      import Evaluate
from RCAIDE.Framework.Mission.Functions import Common


# ----------------------------------------------------------------------------------------------------------------------
# Constant_Throttle_Constant_Speed
# ---------------------------------------------------------------------------------------------------------------------- 
 
class Constant_Throttle_Constant_Speed(Evaluate):
    """ Climb at a constant throttle setting and true airspeed. This segment may not always converge as the vehicle 
        could be deficient in thrust. Useful as a check to see the climb rate at the top of climb. 
    """     
    
    def __defaults__(self):
        """ Specific flight segment defaults which can be modified after initializing.
        
            Assumptions:
                None
    
            Source:
                None
        """          
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude_start    = None # Optional
        self.altitude_end      = 10. * Units.km
        self.throttle          = 0.5
        self.air_speed         = None
        self.true_course       = 0.0 * Units.degrees       

        # -------------------------------------------------------------------------------------------------------------- 
        #  Functions specific processes
        # --------------------------------------------------------------------------------------------------------------      
        initialize                         = self.process.initialize  
        initialize.velocities              = RCAIDE.Framework.Mission.Mission.Segments.Climb.Constant_Throttle_Constant_Speed.update_velocity_vector_from_wind_angle
        initialize.conditions              = RCAIDE.Framework.Mission.Mission.Segments.Climb.Constant_Throttle_Constant_Speed.initialize_conditions
        iterate                            = self.process.iterate
        iterate.unknowns.mission           = RCAIDE.Framework.Mission.Mission.Segments.Climb.Constant_Throttle_Constant_Speed.unpack_body_angle
        iterate.differentials_altitude     = RCAIDE.Framework.Mission.Mission.Segments.Climb.Constant_Throttle_Constant_Speed.update_differentials_altitude
        iterate.velocities                 = RCAIDE.Framework.Mission.Mission.Segments.Climb.Constant_Throttle_Constant_Speed.update_velocity_vector_from_wind_angle
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        return

