
# RCAIDE/Analyses/Mission/Segments/Climb/Constant_Dynamic_Pressure_Constant_Angle.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Core             import Units
from RCAIDE.Methods.Missions import Segments as Methods 
from .Unknown_Throttle       import Unknown_Throttle

# ----------------------------------------------------------------------------------------------------------------------
#  SEGMENT
# ---------------------------------------------------------------------------------------------------------------------- 
 
## @ingroup Analyses-Mission-Segments-Climb
class Constant_Dynamic_Pressure_Constant_Angle(Unknown_Throttle):
    """ Climb at a constant dynamic pressure at a constant angle.This segment takes longer to solve than most because 
        it has extra unknowns and residuals
    
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
        #   USER INPUTS
        # -------------------------------------------------------------------------------------------------------------- 
        self.altitude_start            = None # Optional
        self.altitude_end              = 10.  * Units.km
        self.climb_angle               = 3.   * Units.degrees
        self.dynamic_pressure          = None
        self.true_course_angle         = 0.0 * Units.degrees
        
        # --------------------------------------------------------------
        #   State
        # --------------------------------------------------------------
        
        # initials and unknowns
        ones_row = self.state.ones_row        
        self.state.unknowns.altitudes  = ones_row(1) * 0.0
        self.state.residuals.forces    = ones_row(3) * 0.0        
        
        # -------------------------------------------------------------------------------------------------------------- 
        #   SOLVING PROCESS
        # --------------------------------------------------------------------------------------------------------------  
        initialize                         = self.process.initialize
        initialize.conditions              = Methods.Climb.Constant_Dynamic_Pressure_Constant_Angle.initialize_conditions_unpack_unknowns
        
        # Unpack Unknowns
        iterate                            = self.process.iterate
        iterate.unknowns.mission           = Methods.Climb.Constant_Dynamic_Pressure_Constant_Angle.initialize_conditions_unpack_unknowns 
        iterate.conditions.differentials   = Methods.Climb.Optimized.update_differentials 
        iterate.residuals.total_forces     = Methods.Climb.Constant_Dynamic_Pressure_Constant_Angle.residual_total_forces        
    
        return
       