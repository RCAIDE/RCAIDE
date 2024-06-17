## @ingroup Framework-Mission-Segments-Climb
# RCAIDE/Framework/Mission/Segments/Climb/Constant_CAS_Constant_Rate.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Core                           import Units 
from RCAIDE.Framework.Mission.Segments.Evaluate      import Evaluate
from RCAIDE.Library.Mission                          import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Constant CAS Constant Rate
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Framework-Mission-Segments-Climb
class Constant_CAS_Constant_Rate(Evaluate):
    """ Climb at a constant Calibrated Airspeed (CAS) at a constant rate. 
    """       
    
    def __defaults__(self): 
        """ This sets the default solver flow. Anything in here can be modified after initializing a segment.
    
            Assumptions:
            None
    
            Source:
            None
    
            Args:
            None
    
            Returns:
            None
        """  
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   User Inputs
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude_start       = None # Optional
        self.altitude_end         = 10. * Units.km
        self.climb_rate           = 3.  * Units.m / Units.s
        self.calibrated_air_speed = None
        self.true_course_angle    = 0.0 * Units.degrees  
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------  
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = Segments.Climb.Constant_CAS_Constant_Rate.initialize_conditions  
        iterate                            = self.process.iterate
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        
        return
       
