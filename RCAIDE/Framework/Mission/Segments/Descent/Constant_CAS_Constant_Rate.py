# RCAIDE/Framework/Mission/Segments/Descent/Constant_CAS_Constant_Rate.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports
from RCAIDE.Framework.Core                       import Units 
from RCAIDE.Framework.Mission.Segments.Evaluate  import Evaluate 
from RCAIDE.Library.Mission                      import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------  
#  Constant_CAS_Constant_Rate
# ----------------------------------------------------------------------------------------------------------------------  
class Constant_CAS_Constant_Rate(Evaluate):
    """Descend at a constant Calibrated Airspeed (EAS) at a constant rate."""
    
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
        self.altitude_start      = None # Optional
        self.altitude_end        = 10. * Units.km
        self.descent_rate        = 3.  * Units.m / Units.s
        self.calibrated_airspeed = 100 * Units.m / Units.s
        self.true_course         = 0.0 * Units.degrees                                 
        
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------  
        initialize                         = self.process.initialize  
        initialize.differentials_altitude  = Common.Initialize.differentials_altitude
        initialize.conditions              = Segments.Descent.Constant_CAS_Constant_Rate.initialize_conditions
        iterate                            = self.process.iterate   
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation        
       
        return

