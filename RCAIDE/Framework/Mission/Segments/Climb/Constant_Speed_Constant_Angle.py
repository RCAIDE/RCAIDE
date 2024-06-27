## @ingroup Framework-Mission-Segments-Climb
# RCAIDE/Framework/Mission/Segments/Climb/Constant_Speed_Constant_Angle.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Core                           import Units 
from RCAIDE.Framework.Mission.Segments.Evaluate      import Evaluate
from RCAIDE.Library.Mission                          import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Speed_Constant_Angle
# ---------------------------------------------------------------------------------------------------------------------- 

## @ingroup Framework-Mission-Segments-Climb
class Constant_Speed_Constant_Angle(Evaluate):
    """ A basic constant true airspeed climb at a constant angle. Usually used for certification to ensure a vehicle
        can clear and obstacle. 
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
        self.altitude_start    = None # Optional
        self.altitude_end      = 10. * Units.km
        self.climb_angle       = 3.  * Units.deg
        self.air_speed         = 100 * Units.m / Units.s
        self.true_course_angle = 0.0 * Units.degrees       
                
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------   
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = Segments.Climb.Constant_Speed_Constant_Angle.initialize_conditions  
        iterate                            = self.process.iterate
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation   
    
        return
       