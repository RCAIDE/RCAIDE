## @ingroup Frameworks-Mission-Segments-Cruise 
# RCAIDE/Frameworks/Mission/Segments/Cruise/Constant_Throttle_Constant_Altitude.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Frameworks.Mission.Segments.Evaluate   import Evaluate 
from RCAIDE.Frameworks.Core                                 import Units   
from RCAIDE.Library.Methods.Mission                      import Common,Segments
from RCAIDE.Frameworks.Analyses                          import Process  

# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Throttle_Constant_Altitude
# ----------------------------------------------------------------------------------------------------------------------  

## @ingroup Frameworks-Mission-Segments-Cruise
class Constant_Throttle_Constant_Altitude(Evaluate):
    """ Vehicle flies at a set throttle setting. Allows a vehicle to do a level acceleration.
    
        Assumptions:
        None
        
        Source:
        None
    """           
    
    
    # ------------------------------------------------------------------
    #   Data Defaults
    # ------------------------------------------------------------------  

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
        iterate.conditions.planet_position = Common.Update.planet_position    
        iterate.residuals.total_forces     = Common.Residuals.level_flight_forces  
        iterate.residuals.velocity         = Segments.Cruise.Constant_Throttle_Constant_Altitude.solve_velocity
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation  
        iterate.unknowns.acceleration      = Segments.Cruise.Constant_Throttle_Constant_Altitude.unpack_unknowns  

        return