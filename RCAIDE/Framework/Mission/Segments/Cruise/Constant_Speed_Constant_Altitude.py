## @ingroup Framework-Mission-Segments-Cruise 
# RCAIDE/Framework/Mission/Segments/Cruise/Constant_Speed_Constant_Altitude.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Framework.Mission.Segments.Evaluate   import Evaluate 
from RCAIDE.Framework.Core                                 import Units   
from RCAIDE.Library.Mission                      import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Speed_Constant_Altitude
# ----------------------------------------------------------------------------------------------------------------------  

## @ingroup Framework-Mission-Segments-Cruise
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
        self.true_course_angle = 0.0 * Units.degrees  

        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # -------------------------------------------------------------------------------------------------------------- 
        initialize                         = self.process.initialize  
        initialize.conditions              = Segments.Cruise.Constant_Speed_Constant_Altitude.initialize_conditions  
        iterate                            = self.process.iterate   
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
 
        return

