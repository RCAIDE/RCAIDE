## @ingroup Framework-Mission-Segments-Cruise 
# RCAIDE/Framework/Mission/Segments/Cruise/Constant_Speed_Constant_Altitude_Loiter.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Mission.Segments.Evaluate   import Evaluate
from RCAIDE.Framework.Core                                 import Units
from RCAIDE.Library.Methods.Mission                      import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Speed_Constant_Altitude_Loiter
# ---------------------------------------------------------------------------------------------------------------------- 
 
## @ingroup Framework-Mission-Segments-Cruise
class Constant_Speed_Constant_Altitude_Loiter(Evaluate):
    """ Fixed true airspeed and altitude for a fixed time.
        This is useful aircraft who need to station keep.
    
        Assumptions:
        Built off of a constant speed constant altitude segment
        
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
        self.time              = 1.0 * Units.sec
        self.true_course_angle = 0.0 * Units.degrees        
                
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------      
        initialize                         = self.process.initialize  
        initialize.conditions              = Segments.Cruise.Constant_Speed_Constant_Altitude_Loiter.initialize_conditions 
        iterate                            = self.process.iterate   
        iterate.residuals.total_forces     = Common.Residuals.level_flight_forces 
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation                  
        return

