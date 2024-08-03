# RCAIDE/Framework/Functions/Segments/Cruise/Constant_Pitch_Rate_Constant_Altitude.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Framework.Missions.Mission import Evaluate
from RCAIDE.Reference.Core import Units
from RCAIDE.Reference.Missions.Functions import Common


# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Pitch_Rate_Constant_Altitude
# ----------------------------------------------------------------------------------------------------------------------  
class Constant_Pitch_Rate_Constant_Altitude(Evaluate):
    """ Vehicle flies at a constant pitch rate at a set altitude. This is maneuvering flight.
        This is used in VTOL aircraft which need to transition from one pitch attitude to another.
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
        self.altitude          = None
        self.pitch_rate        = 1.  * Units['rad/s/s']
        self.pitch_initial     = None
        self.pitch_final       = 0.0 * Units['rad']
        self.true_course       = 0.0 * Units.degrees  
 
        # -------------------------------------------------------------------------------------------------------------- 
        #  Functions specific processes
        # --------------------------------------------------------------------------------------------------------------       
        initialize                         = self.process.initialize  
        initialize.conditions              = RCAIDE.Framework.Mission.Mission.Segments.Cruise.Constant_Pitch_Rate_Constant_Altitude.initialize_conditions
        iterate                            = self.process.iterate 
        iterate.unknowns.mission           = Common.Unpack_Unknowns.attitude  
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        
        return

