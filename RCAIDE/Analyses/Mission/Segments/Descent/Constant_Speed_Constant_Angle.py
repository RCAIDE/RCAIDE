## @ingroup Analyses-Mission-Segments-Descent
# RCAIDE/Analyses/Mission/Segments/Descent/Constant_Speed_Constant_Angle.py
# (c) Copyright 2023 Aerospace Research Community LLC
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
#  Constant_Speed_Constant_Angle
# ----------------------------------------------------------------------------------------------------------------------  

## @ingroup Analyses-Mission-Segments-Descent
class Constant_Speed_Constant_Angle(Unknown_Throttle):
    """ Fixed at a true airspeed the vehicle will descend at a constant angle.
    
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
        #   USER INPUTS
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude_start    = None # Optional
        self.altitude_end      = 0.0 * Units.km
        self.descent_angle     = 3.  * Units.deg
        self.air_speed         = 100 * Units.m / Units.s
        self.true_course_angle = 0.0 * Units.degrees 
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   SOLVING PROCESS
        # -------------------------------------------------------------------------------------------------------------- 
        initialize            = self.process.initialize
        initialize.conditions = Methods.Descent.Constant_Speed_Constant_Angle.initialize_conditions
       
        return

