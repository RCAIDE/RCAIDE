## @ingroup Analyses-Mission-Segments-Descent
# RCAIDE/Analyses/Mission/Segments/Descent/Linear_Mach_Constant_Rate.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

from RCAIDE.Methods.Missions                                 import Segments as Methods
from RCAIDE.Analyses.Mission.Segments.Climb.Unknown_Throttle import Unknown_Throttle
from RCAIDE.Core                                             import Units

# ----------------------------------------------------------------------------------------------------------------------  
#  Linear_Mach_Constant_Rate
# ----------------------------------------------------------------------------------------------------------------------  

## @ingroup Analyses-Mission-Segments-Descent
class Linear_Mach_Constant_Rate(Unknown_Throttle):
    """ Change Mach numbers during a descent while descending at a constant rate. The Mach number changes linearly
        throughout the descent.
    
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
        self.altitude_end      = 10. * Units.km
        self.descent_rate      = 3.  * Units.m / Units.s
        self.mach_number_end   = 0.7
        self.mach_number_start = None
        self.true_course_angle = 0.0 * Units.degrees 
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   SOLVING PROCESS
        # -------------------------------------------------------------------------------------------------------------- 
        initialize = self.process.initialize
        initialize.conditions = Methods.Descent.Linear_Mach_Constant_Rate.initialize_conditions

        return

