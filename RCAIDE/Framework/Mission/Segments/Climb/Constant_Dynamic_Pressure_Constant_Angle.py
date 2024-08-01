# RCAIDE/Framework/Functions/Segments/Climb/Constant_Dynamic_Pressure_Constant_Angle.py
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
# Constant_Dynamic_Pressure_Constant_Angle
# ---------------------------------------------------------------------------------------------------------------------- 
class Constant_Dynamic_Pressure_Constant_Angle(Evaluate):
    """ Climb at a constant dynamic pressure at a constant angle.This segment takes longer to solve than most because 
        it has extra unknowns and residuals.
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
        self.altitude_start            = None # Optional
        self.altitude_end              = 10.  * Units.km
        self.climb_angle               = 3.   * Units.degrees
        self.dynamic_pressure          = None
        self.true_course               = 0.0 * Units.degrees
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Functions Specific Unknowns and Residuals
        # --------------------------------------------------------------------------------------------------------------    
        ones_row = self.state.ones_row             
        self.state.residuals.altitude      = ones_row(1) * 0.0
        self.state.unknowns.altitude       = ones_row(1) * 0.0                                         
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Functions specific processes
        # --------------------------------------------------------------------------------------------------------------   
        initialize                         = self.process.initialize
        initialize.conditions              = RCAIDE.Framework.Mission.Mission.Segments.Climb.Constant_Dynamic_Pressure_Constant_Angle.initialize_conditions_unpack_unknowns
        iterate                            = self.process.iterate 
        iterate.unknowns.mission           = Common.Unpack_Unknowns.attitude
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.unknowns.kinematics        = RCAIDE.Framework.Mission.Mission.Segments.Climb.Constant_Dynamic_Pressure_Constant_Angle.initialize_conditions_unpack_unknowns
        iterate.conditions.differentials   = RCAIDE.Framework.Mission.Mission.Segments.Climb.Constant_Dynamic_Pressure_Constant_Angle.update_differentials
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        iterate.residuals.altitude         = RCAIDE.Framework.Mission.Mission.Segments.Climb.Constant_Dynamic_Pressure_Constant_Angle.residual_altitude
        return
       