## @ingroup Framework-Mission-Segments-Climb
# RCAIDE/Framework/Mission/Segments/Climb/Constant_Mach_Linear_Altitude.py
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
# Constant_Mach_Linear_Altitude
# ---------------------------------------------------------------------------------------------------------------------- 

## @ingroup Framework-Mission-Segments-Climb
class Constant_Mach_Linear_Altitude(Evaluate):
    """ Climb at a constant mach number but linearly change altitudes over a distance. 
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
        self.mach              = 0.5
        self.distance          = 10. * Units.km
        self.altitude_start    = None
        self.altitude_end      = None
        self.true_course_angle = 0.0 * Units.degrees     
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------   
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = Segments.Climb.Constant_Mach_Linear_Altitude.initialize_conditions  
        iterate                            = self.process.iterate
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation   
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics


        return

