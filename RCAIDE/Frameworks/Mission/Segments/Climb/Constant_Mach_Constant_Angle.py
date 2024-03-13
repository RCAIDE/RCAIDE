## @ingroup Frameworks-Mission-Segments-Climb
# RCAIDE/Frameworks/Mission/Segments/Climb/Constant_Mach_Constant_Angle.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Frameworks.Core                                     import Units 
from RCAIDE.Frameworks.Mission.Segments.Evaluate       import Evaluate
from RCAIDE.Library.Methods.Mission                          import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
# Constant_Mach_Constant_Angle
# ---------------------------------------------------------------------------------------------------------------------- 

## @ingroup Frameworks-Mission-Segments-Climb
class Constant_Mach_Constant_Angle(Evaluate):
    """ Climb at a constant mach number and at a constant angle.
        This segment takes longer to solve than most because it has extra unknowns and residuals
    
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
        self.altitude_start    = None # Optional
        self.altitude_end      = 10. * Units.km
        self.climb_angle       = 3.  * Units.deg
        self.mach_number       = None
        self.true_course_angle = 0.0 * Units.degrees 

        # -------------------------------------------------------------------------------------------------------------- 
        #  Unique Mission Unknowns and Residuals
        # --------------------------------------------------------------------------------------------------------------  
        ones_row = self.state.ones_row        
        self.state.unknowns.altitude   = ones_row(1) * 0.0   
        self.state.residuals.altitude  = ones_row(1) * 0.0   
    
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------   
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = Segments.Climb.Constant_Mach_Constant_Angle.initialize_conditions  
        iterate                            = self.process.iterate
        iterate.residuals.total_forces     = Segments.Climb.Constant_Mach_Constant_Angle.residual_total_forces 
        iterate.conditions.differentials   = Segments.Climb.Constant_Mach_Constant_Angle.update_differentials 
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation
        iterate.unknowns.kinematics        = Segments.Climb.Constant_Mach_Constant_Angle.initialize_conditions 
          
        return

