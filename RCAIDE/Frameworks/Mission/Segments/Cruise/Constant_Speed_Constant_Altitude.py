## @ingroup Frameworks-Mission-Segments-Cruise 
# RCAIDE/Frameworks/Mission/Segments/Cruise/Constant_Speed_Constant_Altitude.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Frameworks.Mission.Segments.Evaluate   import Evaluate 
from RCAIDE.Frameworks.Core                                 import Units   
from RCAIDE.Library.Methods.Mission                      import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Speed_Constant_Altitude
# ----------------------------------------------------------------------------------------------------------------------  

## @ingroup Frameworks-Mission-Segments-Cruise
class Constant_Speed_Constant_Altitude(Evaluate):
    """ Fixed true airspeed and altitude and a set distance.
        Most other cruise segments are built off this segment. The most simple segment you can fly.
    
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
        # User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude          = None
        self.air_speed         = None
        self.distance          = 10. * Units.km
        self.true_course_angle = 0.0 * Units.degrees  

        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # -------------------------------------------------------------------------------------------------------------- 
        initialize                         = self.process.initialize  
        initialize.conditions              = Segments.Cruise.Constant_Speed_Constant_Altitude.initialize_conditions  
        iterate                            = self.process.iterate   
        iterate.residuals.total_forces     = Common.Residuals.level_flight_forces 
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation          
 
        return

