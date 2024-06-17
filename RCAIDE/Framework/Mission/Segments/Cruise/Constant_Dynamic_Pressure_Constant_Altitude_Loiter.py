## @ingroup Framework-Mission-Segments-Cruise 
# RCAIDE/Framework/Mission/Segments/Cruise/Constant_Dynamic_Pressure_Constant_Altitude_Loiter.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Mission.Segments.Evaluate   import Evaluate 
from RCAIDE.Framework.Core                                 import Units   
from RCAIDE.Library.Mission                      import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Dynamic_Pressure_Constant_Altitude_Loiter
# ----------------------------------------------------------------------------------------------------------------------  

## @ingroup Framework-Mission-Segments-Cruise
class Constant_Dynamic_Pressure_Constant_Altitude_Loiter(Evaluate):
    """ Vehicle flies at a constant dynamic pressure at a set altitude for a fixed time.
    """           
    
    def __defaults__(self):
        """ This sets the default solver flow. Anything in here can be modified after initializing a segment.
    
            Assumptions:
                None
    
            Source:
                self : mission segment [-]
    
            Args:
                None
    
            Returns:
                None
        """           
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude          = 0.0
        self.dynamic_pressure  = None
        self.time              = 1.0 * Units.sec
        self.true_course_angle = 0.0 * Units.degrees 
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------    
        initialize                         = self.process.initialize  
        initialize.conditions              = Segments.Cruise.Constant_Dynamic_Pressure_Constant_Altitude_Loiter.initialize_conditions
        iterate                            = self.process.iterate   
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        return

