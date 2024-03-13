## @ingroup Frameworks-Mission-Segments-Descent
# RCAIDE/Frameworks/Mission/Segments/Descent/Linear_Mach_Constant_Rate.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 
from RCAIDE.Frameworks.Core                                 import Units 
from RCAIDE.Frameworks.Mission.Segments.Evaluate   import Evaluate 
from RCAIDE.Library.Methods.Mission                      import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------  
#  Linear_Mach_Constant_Rate
# ----------------------------------------------------------------------------------------------------------------------  

## @ingroup Frameworks-Mission-Segments-Descent
class Linear_Mach_Constant_Rate(Evaluate):
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
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude_start    = None # Optional
        self.altitude_end      = 10. * Units.km
        self.descent_rate      = 3.  * Units.m / Units.s
        self.mach_number_end   = 0.7
        self.mach_number_start = None
        self.true_course_angle = 0.0 * Units.degrees  
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # -------------------------------------------------------------------------------------------------------------- 
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = Segments.Descent.Linear_Mach_Constant_Rate.initialize_conditions
        iterate                            = self.process.iterate   
        iterate.residuals.total_forces     = Common.Residuals.climb_descent_forces 
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation        

        return

