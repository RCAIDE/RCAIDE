# RCAIDE/Framework/Functions/Segments/Single_Point/Set_Speed_Set_Throttle.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports   
from RCAIDE.Library.Methods.skip                     import skip 
from RCAIDE.Reference.Core import Units
from RCAIDE.Framework.Missions.Mission import Evaluate
from RCAIDE.Reference.Missions.Functions import Common


# ----------------------------------------------------------------------------------------------------------------------
#  Set_Speed_Set_Throttle
# ---------------------------------------------------------------------------------------------------------------------- 
class Set_Speed_Set_Throttle(Evaluate):
    """ This is a segment that is solved using a single point. A snapshot in time.
        We fix the speed and throttle. Acceleration is solved from those. 
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
        self.altitude                                = None
        self.air_speed                               = 10. * Units['km/hr']
        self.throttle                                = 1.
        self.acceleration_z                          = 0. # note that down is positive
        self.state.numerics.number_of_control_points = 1  

        # -------------------------------------------------------------------------------------------------------------- 
        #  Functions specific processes
        # --------------------------------------------------------------------------------------------------------------             
        initialize                               = self.process.initialize 
        initialize.expand_state                  = skip
        initialize.differentials                 = skip
        initialize.conditions                    = RCAIDE.Framework.Mission.Mission.Segments.Single_Point.Set_Speed_Set_Throttle.initialize_conditions
        iterate                                  = self.process.iterate 
        iterate.initials.energy                  = skip    
        iterate.unknowns.mission                 = RCAIDE.Framework.Mission.Mission.Segments.Single_Point.Set_Speed_Set_Throttle.unpack_unknowns
        iterate.conditions.differentials         = skip 
        iterate.conditions.planet_position       = skip    
        iterate.conditions.acceleration          = skip
        iterate.conditions.angular_acceleration  = skip 
        iterate.conditions.weights               = skip 
        iterate.residuals.flight_dynamics        = Common.Residuals.flight_dynamics
        post_process                             = self.process.post_process 
        post_process.inertial_position           = skip    
                
                
        return

