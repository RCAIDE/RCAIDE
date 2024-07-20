# RCAIDE/Framework/Mission/Segments/Cruise/Constant_Pitch_Rate_Constant_Altitude.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Framework.Mission.Segments.Evaluate  import Evaluate 
from RCAIDE.Framework.Core                       import Units   
from RCAIDE.Library.Mission.Segments             import Cruise
from RCAIDE.Library.Mission                      import Common
# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Pitch_Rate_Constant_Altitude
# ----------------------------------------------------------------------------------------------------------------------  
class Constant_Pitch_Rate_Constant_Altitude(Evaluate):
    """ Vehicle flies at a constant pitch rate at a set altitude. This is maneuvering flight.
        This is used in VTOL aircraft which need to transition from one pitch attitude to another.
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
        self.altitude          = None
        self.pitch_rate        = 1.  * Units['rad/s/s']
        self.pitch_initial     = None
        self.pitch_final       = 0.0 * Units['rad']
        self.true_course       = 0.0 * Units.degrees  
 
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------       
        initialize                         = self.process.initialize  
        initialize.conditions              = Cruise.Constant_Pitch_Rate_Constant_Altitude.initialize_conditions  
        iterate                            = self.process.iterate 
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation  
        iterate.unknowns.controls          = Common.Unpack_Unknowns.control_surfaces
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        
        return

