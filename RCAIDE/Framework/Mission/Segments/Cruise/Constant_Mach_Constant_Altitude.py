## @ingroup Framework-Mission-Segments-Cruise 
# RCAIDE/Framework/Mission/Segments/Cruise/Constant_Mach_Constant_Altitude.py
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
# Constant_Mach_Constant_Altitude
# ----------------------------------------------------------------------------------------------------------------------  

## @ingroup Framework-Mission-Segments-Cruise
class Constant_Mach_Constant_Altitude(Evaluate):
    """ Vehicle flies at a constant Mach number at a set altitude for a fixed distance
    
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
        self.altitude           = None
        self.mach_number        = None
        self.distance           = 10. * Units.km
        self.true_course_angle  = 0.0 * Units.degrees     
    
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------   
        initialize                         = self.process.initialize  
        initialize.conditions              = Segments.Cruise.Constant_Mach_Constant_Altitude.initialize_conditions
        iterate                            = self.process.iterate       
        iterate.residuals.total_forces     = Common.Residuals.level_flight_forces 
        iterate.unknowns.mission           = Common.Unpack_Unknowns.orientation   

        return

