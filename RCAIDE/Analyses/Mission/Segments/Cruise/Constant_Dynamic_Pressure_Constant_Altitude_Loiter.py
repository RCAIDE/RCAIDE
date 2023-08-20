## @ingroup Analyses-Mission-Segments-Cruise 
# RCAIDE/Analyses/Mission/Segments/Cruise/Constant_Dynamic_Pressure_Constant_Altitude_Loiter.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Core                       import Units
from RCAIDE.Methods.Missions           import Segments as Methods 
from .Constant_Speed_Constant_Altitude import Constant_Speed_Constant_Altitude

# ----------------------------------------------------------------------------------------------------------------------
#  Constant_Dynamic_Pressure_Constant_Altitude_Loiter
# ----------------------------------------------------------------------------------------------------------------------  

## @ingroup Analyses-Mission-Segments-Cruise
class Constant_Dynamic_Pressure_Constant_Altitude_Loiter(Constant_Speed_Constant_Altitude):
    """ Vehicle flies at a constant dynamic pressure at a set altitude for a fixed time.
        This is useful for HALE UAVs like a solar UAV.
    
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
        #   USER INPUTS
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude          = 0.0
        self.dynamic_pressure  = None
        self.time              = 1.0 * Units.sec
        self.true_course_angle = 0.0 * Units.degrees
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   SOLVING PROCESS
        # -------------------------------------------------------------------------------------------------------------- 
        initialize            = self.process.initialize
        initialize.conditions = Methods.Cruise.Constant_Dynamic_Pressure_Constant_Altitude_Loiter.initialize_conditions


        return

