# RCAIDE/Framework/Functions/Segments/Cruise/Constant_Acceleration_Constant_Altitude.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Framework.Mission.Segments.Evaluate  import Evaluate 
from RCAIDE.Framework.Core                       import Units   
from RCAIDE.Framework.Mission.Functions import Common


# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Acceleration_Constant_Altitude
# ---------------------------------------------------------------------------------------------------------------------- 
class Constant_Acceleration_Constant_Altitude(Evaluate):
    """ Vehicle accelerates at a constant rate between two airspeeds. 
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
        self.acceleration      = 1.  * Units['m/s/s']
        self.air_speed_start   = None
        self.air_speed_end     = 1.0 * Units['m/s']
        self.true_course       = 0.0 * Units.degrees       
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Functions specific processes
        # --------------------------------------------------------------------------------------------------------------   
        initialize                         = self.process.initialize 
        initialize.conditions              = RCAIDE.Framework.Mission.Mission.Segments.Cruise.Constant_Acceleration_Constant_Altitude.initialize_conditions
        iterate                            = self.process.iterate  
        iterate.unknowns.mission           = Common.Unpack_Unknowns.attitude
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        return

