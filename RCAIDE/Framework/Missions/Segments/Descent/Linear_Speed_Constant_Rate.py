# RCAIDE/Framework/Functions/Segments/Descent/Linear_Speed_Constant_Rate.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Core                       import Units 
from RCAIDE.Framework.Mission.Segments.Evaluate  import Evaluate 
from RCAIDE.Framework.Mission.Functions import Common


# ----------------------------------------------------------------------------------------------------------------------
#  Linear_Speed_Constant_Rate
# ----------------------------------------------------------------------------------------------------------------------
class Linear_Speed_Constant_Rate(Evaluate):
    """ Linearly change true airspeed while climbing at a constant rate. 
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
        self.descent_rate      = 3.  * Units.m / Units.s
        self.air_speed_start   = None
        self.air_speed_end     = 200 * Units.m / Units.s
        self.true_course       = 0.0 * Units.degrees     
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Functions specific processes
        # -------------------------------------------------------------------------------------------------------------- 
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = RCAIDE.Framework.Mission.Mission.Segments.Descent.Linear_Speed_Constant_Rate.initialize_conditions
        iterate                            = self.process.iterate   
        iterate.unknowns.mission           = Common.Unpack_Unknowns.attitude
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics

        return

