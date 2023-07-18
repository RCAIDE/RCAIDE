## @ingroup Analyses-Mission-Segments-Descent
# RCAIDE/Analyses/Mission/Segments/Descent/Constant_CAS_Constant_Rate.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports
from RCAIDE.Methods.Missions                                 import Segments as Methods 
from RCAIDE.Analyses.Mission.Segments.Climb.Unknown_Throttle import Unknown_Throttle 
from RCAIDE.Core                                             import Units

# ----------------------------------------------------------------------------------------------------------------------  
#  Constant_CAS_Constant_Rate
# ----------------------------------------------------------------------------------------------------------------------  

## @ingroup Analyses-Mission-Segments-Descent
class Constant_CAS_Constant_Rate(Unknown_Throttle):
    
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
        #   USER INPUTS
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude_start      = None # Optional
        self.altitude_end        = 10. * Units.km
        self.descent_rate        = 3.  * Units.m / Units.s
        self.calibrated_airspeed = 100 * Units.m / Units.s
        self.true_course_angle   = 0.0 * Units.degrees 
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   SOLVING PROCESS
        # --------------------------------------------------------------------------------------------------------------  
        initialize = self.process.initialize
        initialize.conditions = Methods.Descent.Constant_CAS_Constant_Rate.initialize_conditions
       
        return

