# RCAIDE/Framework/Functions/Segments/Cruise/Constant_Speed_Constant_Altitude.py
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
#  Constant_Speed_Constant_Altitude
# ----------------------------------------------------------------------------------------------------------------------  
class Constant_Speed_Constant_Altitude(Evaluate):
    """ Fixed true airspeed and altitude and a set distance. 
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
        self.distance          = 10. * Units.km
        self.true_course       = 0.0 * Units.degrees  

        # -------------------------------------------------------------------------------------------------------------- 
        #  Functions specific processes
        # -------------------------------------------------------------------------------------------------------------- 
        initialize                         = self.process.initialize  
        initialize.conditions              = RCAIDE.Framework.Mission.Mission.Segments.Cruise.Constant_Speed_Constant_Altitude.initialize_conditions
        iterate                            = self.process.iterate   
        iterate.unknowns.mission           = Common.Unpack_Unknowns.attitude
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
 
        return
