## @ingroup Analyses-Mission-Segments-Cruise 
# RCAIDE/Analyses/Mission/Segments/Cruise/Constant_Pitch_Rate_Constant_Altitude.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports  
from RCAIDE.Analyses.Mission.Segments.Evaluate   import Evaluate 
from RCAIDE.Core                                 import Units   
from RCAIDE.Methods.Mission.Segments             import Cruise
from RCAIDE.Methods.Mission                      import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Pitch_Rate_Constant_Altitude
# ----------------------------------------------------------------------------------------------------------------------  

## @ingroup Analyses-Mission-Segments-Cruise
class Constant_Pitch_Rate_Constant_Altitude(Evaluate):
    """ Vehicle flies at a constant pitch rate at a set altitude. This is maneuvering flight.
        This is used in VTOL aircraft which need to transition from one pitch attitude to another.
    
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
        self.altitude          = None
        self.pitch_rate        = 1.  * Units['rad/s/s']
        self.pitch_initial     = None
        self.pitch_final       = 0.0 * Units['rad']
        self.true_course_angle = 0.0 * Units.degrees  
 
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------       
        initialize                         = self.process.initialize  
        initialize.conditions              = Cruise.Constant_Pitch_Rate_Constant_Altitude.initialize_conditions  
        iterate                            = self.process.iterate 
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation  
        iterate.residuals.total_forces     = Common.Residuals.level_flight_forces
        
        return
