# RCAIDE/Framework/Functions/Segments/Climb/Constant_Mach_Constant_Angle.py
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
# Constant_Mach_Constant_Angle
# ---------------------------------------------------------------------------------------------------------------------- 
class Constant_Mach_Constant_Angle(Evaluate):
    """ Climb at a constant mach number and at a constant angle.
        This segment takes longer to solve than most because it has extra unknowns and residuals 
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
        self.climb_angle       = 3.  * Units.deg
        self.mach_number       = None
        self.true_course       = 0.0 * Units.degrees 

        # -------------------------------------------------------------------------------------------------------------- 
        #  Unique Functions Unknowns and Residuals
        # --------------------------------------------------------------------------------------------------------------  
        ones_row = self.state.ones_row    
        self.state.unknowns.altitude   = ones_row(1) * 0.0   
        self.state.residuals.altitude  = ones_row(1) * 0.0   
    
        # -------------------------------------------------------------------------------------------------------------- 
        #  Functions specific processes
        # --------------------------------------------------------------------------------------------------------------   
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = RCAIDE.Framework.Mission.Mission.Segments.Climb.Constant_Mach_Constant_Angle.initialize_conditions
        iterate                            = self.process.iterate
        iterate.residuals.flight_altitude  = RCAIDE.Framework.Mission.Mission.Segments.Climb.Constant_Mach_Constant_Angle.altitude_residual
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        iterate.conditions.differentials   = RCAIDE.Framework.Mission.Mission.Segments.Climb.Constant_Mach_Constant_Angle.update_differentials
        iterate.unknowns.mission           = Common.Unpack_Unknowns.attitude
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.unknowns.kinematics        = RCAIDE.Framework.Mission.Mission.Segments.Climb.Constant_Mach_Constant_Angle.initialize_conditions

        return

