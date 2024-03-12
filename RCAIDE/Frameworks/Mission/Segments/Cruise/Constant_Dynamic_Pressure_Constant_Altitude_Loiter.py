## @ingroup Frameworks-Mission-Segments-Cruise 
# RCAIDE/Frameworks/Mission/Segments/Cruise/Constant_Dynamic_Pressure_Constant_Altitude_Loiter.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Frameworks.Mission.Segments.Evaluate   import Evaluate 
from RCAIDE.Core                                 import Units   
from RCAIDE.Methods.Mission                      import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Dynamic_Pressure_Constant_Altitude_Loiter
# ----------------------------------------------------------------------------------------------------------------------  

## @ingroup Frameworks-Mission-Segments-Cruise
class Constant_Dynamic_Pressure_Constant_Altitude_Loiter(Evaluate):
    """ Vehicle flies at a constant dynamic pressure at a set altitude for a fixed time.
        This is useful for HALE UAVs like a solar UAV.
    
        Assumptions:
        Built off of a constant speed constant altitude segment
        
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
        iterate.residuals.total_forces     = Common.Residuals.level_flight_forces 
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation        
        return

