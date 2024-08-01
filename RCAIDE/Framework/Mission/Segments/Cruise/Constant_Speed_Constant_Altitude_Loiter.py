# RCAIDE/Framework/Functions/Segments/Cruise/Constant_Speed_Constant_Altitude_Loiter.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Mission.Segments.Evaluate   import Evaluate 
from RCAIDE.Framework.Core                                 import Units   
from RCAIDE.Framework.Mission.Functions import Common


# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Speed_Constant_Altitude_Loiter
# ---------------------------------------------------------------------------------------------------------------------- 
class Constant_Speed_Constant_Altitude_Loiter(Evaluate):
    """ Fixed true airspeed and altitude for a fixed time. This is useful aircraft who need to station keep. 
    """        
    
    def __defaults__(self):
        """ Specific flight segment defaults which can be modified after initializing.
        
            Assumptions:
                None
    
            Source:
                None
        """           
        
        # -------------------------------------------------------------------------------------------------------------- 
        # User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude          = None
        self.air_speed         = None
        self.time              = 1.0 * Units.sec
        self.true_course       = 0.0 * Units.degrees        
                
        # -------------------------------------------------------------------------------------------------------------- 
        #  Functions specific processes
        # --------------------------------------------------------------------------------------------------------------      
        initialize                         = self.process.initialize  
        initialize.conditions              = RCAIDE.Framework.Mission.Mission.Segments.Cruise.Constant_Speed_Constant_Altitude_Loiter.initialize_conditions
        iterate                            = self.process.iterate   
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.unknowns.mission           = Common.Unpack_Unknowns.attitude
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        return

