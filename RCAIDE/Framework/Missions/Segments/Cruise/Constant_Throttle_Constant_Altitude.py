# RCAIDE/Framework/Functions/Segments/Cruise/Constant_Throttle_Constant_Altitude.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Framework.Missions.Segments.Evaluate   import Evaluate
from RCAIDE.Framework.Core                        import Units   
from RCAIDE.Framework.Analyses                    import Process  
from RCAIDE.Framework.Mission.Functions import Common


# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Throttle_Constant_Altitude
# ----------------------------------------------------------------------------------------------------------------------   
class Constant_Throttle_Constant_Altitude(Evaluate):
    """ Vehicle flies at a set throttle setting. Allows a vehicle to do a level acceleration. 
    """            
    def __defaults__(self):
        """ Specific flight segment defaults which can be modified after initializing.
        
            Assumptions:
                None
    
            Source:
                None
        """           
        
        # -------------------------------------------------------------------------------------------------------------- 
        # User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.throttle          = None
        self.altitude          = None
        self.air_speed_start   = None
        self.air_speed_end     = 0.0 
        self.true_course       = 0.0 * Units.degrees   
     
        # -------------------------------------------------------------------------------------------------------------- 
        #  Functions specific processes
        # --------------------------------------------------------------------------------------------------------------    
        initialize                         = self.process.initialize  
        initialize.conditions              = RCAIDE.Framework.Mission.Mission.Segments.Cruise.Constant_Throttle_Constant_Altitude.initialize_conditions
        iterate                            = self.process.iterate             

        # Update Conditions
        iterate.conditions = Process()
        iterate.conditions.differentials   = Common.Update.differentials_time 
        iterate.conditions.velocity        = RCAIDE.Framework.Mission.Mission.Segments.Cruise.Constant_Throttle_Constant_Altitude.integrate_velocity
        iterate.conditions.acceleration    = Common.Update.acceleration   
        iterate.conditions.altitude        = Common.Update.altitude
        iterate.conditions.atmosphere      = Common.Update.atmosphere
        iterate.conditions.gravity         = Common.Update.gravity
        iterate.conditions.freestream      = Common.Update.freestream
        iterate.conditions.orientations    = Common.Update.orientations
        iterate.conditions.energy          = Common.Update.thrust
        iterate.conditions.aerodynamics    = Common.Update.aerodynamics
        iterate.conditions.stability       = Common.Update.stability
        iterate.conditions.weights         = Common.Update.weights
        iterate.conditions.forces          = Common.Update.forces
        iterate.conditions.moments         = Common.Update.moments
        iterate.conditions.planet_position = Common.Update.planet_position
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        iterate.residuals.velocity         = RCAIDE.Framework.Mission.Mission.Segments.Cruise.Constant_Throttle_Constant_Altitude.solve_velocity
        iterate.unknowns.mission           = Common.Unpack_Unknowns.attitude  
        iterate.unknowns.acceleration      = RCAIDE.Framework.Mission.Mission.Segments.Cruise.Constant_Throttle_Constant_Altitude.unpack_unknowns

        return