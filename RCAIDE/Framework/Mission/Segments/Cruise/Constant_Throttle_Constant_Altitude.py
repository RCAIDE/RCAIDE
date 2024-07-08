# RCAIDE/Framework/Mission/Segments/Cruise/Constant_Throttle_Constant_Altitude.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Framework.Mission.Segments.Evaluate   import Evaluate 
from RCAIDE.Framework.Core                        import Units   
from RCAIDE.Framework.Analyses                    import Process  
from RCAIDE.Library.Mission                       import Common,Segments

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
        self.true_course_angle = 0.0 * Units.degrees  

        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission Specific Unknowns and Residuals 
        # --------------------------------------------------------------------------------------------------------------  
        self.state.residuals.final_velocity_error = 0.0
     
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------    
        initialize                         = self.process.initialize  
        initialize.conditions              = Segments.Cruise.Constant_Throttle_Constant_Altitude.initialize_conditions      
        iterate                            = self.process.iterate             

        # Update Conditions
        iterate.conditions = Process()
        iterate.conditions.differentials   = Common.Update.differentials_time 
        iterate.conditions.velocity        = Segments.Cruise.Constant_Throttle_Constant_Altitude.integrate_velocity     
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
        iterate.residuals.velocity         = Segments.Cruise.Constant_Throttle_Constant_Altitude.solve_velocity
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation  
        iterate.unknowns.acceleration      = Segments.Cruise.Constant_Throttle_Constant_Altitude.unpack_unknowns  

        return