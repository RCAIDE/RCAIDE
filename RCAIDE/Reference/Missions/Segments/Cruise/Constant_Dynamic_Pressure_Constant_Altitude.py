# RCAIDE/Framework/Functions/Segments/Cruise/Constant_Dynamic_Pressure_Constant_Altitude.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Reference.Missions.Segments.Evaluate import Evaluate
from RCAIDE.Reference.Core import Units
from RCAIDE.Reference.Missions.Functions import Common


# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Dynamic_Pressure_Constant_Altitude
# ----------------------------------------------------------------------------------------------------------------------  
class Constant_Dynamic_Pressure_Constant_Altitude(Evaluate):
    """ Vehicle flies at a constant dynamic pressure at a set altitude for a fixed distance 
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
        self.altitude          = 0.0
        self.dynamic_pressure  = None  
        self.distance          = 1.0 * Units.km
        self.true_course       = 0.0 * Units.degrees              
    
        # -------------------------------------------------------------------------------------------------------------- 
        #  Functions specific processes
        # --------------------------------------------------------------------------------------------------------------      
        initialize                         = self.process.initialize  
        initialize.conditions              = RCAIDE.Framework.Mission.Mission.Segments.Cruise.Constant_Dynamic_Pressure_Constant_Altitude.initialize_conditions
        iterate                            = self.process.iterate   
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.unknowns.mission           = Common.Unpack_Unknowns.attitude  
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics

        return
