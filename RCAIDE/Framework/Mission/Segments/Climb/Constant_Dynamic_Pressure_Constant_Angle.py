## @ingroup Analyses-Mission-Segments-Climb
# RCAIDE/Framework/Analyses/Mission/Segments/Climb/Constant_Dynamic_Pressure_Constant_Angle.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Framework.Core                                     import Units 
from RCAIDE.Framework.Mission.Segments.Evaluate       import Evaluate
from RCAIDE.Library.Mission                          import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
# Constant_Dynamic_Pressure_Constant_Angle
# ---------------------------------------------------------------------------------------------------------------------- 
 
## @ingroup Analyses-Mission-Segments-Climb
class Constant_Dynamic_Pressure_Constant_Angle(Evaluate):
    """ Climb at a constant dynamic pressure at a constant angle.This segment takes longer to solve than most because 
        it has extra unknowns and residuals
    
        Assumptions:
        None
        
        Source:
        None
    """       
    
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
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude_start            = None # Optional
        self.altitude_end              = 10.  * Units.km
        self.climb_angle               = 3.   * Units.degrees
        self.dynamic_pressure          = None
        self.true_course               = 0.0 * Units.degrees
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission Specific Unknowns and Residuals 
        # --------------------------------------------------------------------------------------------------------------    
        ones_row = self.state.ones_row             
        self.state.residuals.altitude      = ones_row(1) * 0.0
        self.state.unknowns.altitude       = ones_row(1) * 0.0                                         
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------   
        initialize                         = self.process.initialize
        initialize.conditions              = Segments.Climb.Constant_Dynamic_Pressure_Constant_Angle.initialize_conditions_unpack_unknowns 
        iterate                            = self.process.iterate 
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.unknowns.kinematics        = Segments.Climb.Constant_Dynamic_Pressure_Constant_Angle.initialize_conditions_unpack_unknowns
        iterate.conditions.differentials   = Segments.Climb.Constant_Dynamic_Pressure_Constant_Angle.update_differentials 
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        iterate.residuals.altitude         = Segments.Climb.Constant_Dynamic_Pressure_Constant_Angle.residual_altitude
        return
       