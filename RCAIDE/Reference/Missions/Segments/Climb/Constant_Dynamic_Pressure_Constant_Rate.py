# RCAIDE/Framework/Functions/Segments/Climb/Constant_Dynamic_Pressure_Constant_Rate.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Reference.Core import Units
from RCAIDE.Framework.Missions.Mission import Evaluate
from RCAIDE.Reference.Missions.Functions import Common


# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Dynamic_Pressure_Constant_Rate
# ---------------------------------------------------------------------------------------------------------------------- 
class Constant_Dynamic_Pressure_Constant_Rate(Evaluate):
    """ Climb at a constant dynamic pressure at a constant rate. 
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
        self.climb_rate        = 3.  * Units.m / Units.s
        self.dynamic_pressure  = None
        self.true_course       = 0.0 * Units.degrees               
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Functions specific processes
        # --------------------------------------------------------------------------------------------------------------  
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = RCAIDE.Framework.Mission.Mission.Segments.Climb.Constant_Dynamic_Pressure_Constant_Rate.initialize_conditions
        iterate                            = self.process.iterate 
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        iterate.unknowns.mission           = Common.Unpack_Unknowns.attitude           
    
        return
       