## @ingroup Frameworks-Mission-Segments-Climb
# RCAIDE/Frameworks/Mission/Segments/Climb/Constant_Dynamic_Pressure_Constant_Rate.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Core                                     import Units 
from RCAIDE.Frameworks.Mission.Segments.Evaluate       import Evaluate
from RCAIDE.Methods.Mission                          import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Dynamic_Pressure_Constant_Rate
# ---------------------------------------------------------------------------------------------------------------------- 

## @ingroup Frameworks-Mission-Segments-Climb
class Constant_Dynamic_Pressure_Constant_Rate(Evaluate):
    """ Climb at a constant dynamic pressure at a constant rate.
    
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
        self.climb_rate        = 3.  * Units.m / Units.s
        self.dynamic_pressure  = None
        self.true_course_angle = 0.0 * Units.degrees               
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------  
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = Segments.Climb.Constant_Dynamic_Pressure_Constant_Rate.initialize_conditions
        iterate                            = self.process.iterate
        iterate.residuals.total_forces     = Common.Residuals.climb_descent_forces 
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation           
    
        return
       