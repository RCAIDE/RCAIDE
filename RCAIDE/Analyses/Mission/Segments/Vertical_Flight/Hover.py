## @ingroup Analyses-Mission-Segments-Vertical_Flight
# RCAIDE/Analyses/Mission/Segments/Vertical_Flight/Hover.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports 
from RCAIDE.Core                                 import Units 
from RCAIDE.Analyses.Mission.Segments.Evaluate   import Evaluate 
from RCAIDE.Methods.Mission                      import Common,Segments

# ----------------------------------------------------------------------------------------------------------------------
#  Hover
# ----------------------------------------------------------------------------------------------------------------------

## @ingroup Analyses-Mission-Segments-Vertical_Flight
class Hover(Evaluate):
    """ A stationary hover for VTOL aircraft. No aerodynamic drag and lift are used, since there is no velocity.
    
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
        
        self.altitude           = None
        self.time               = 1.0 * Units.seconds
        self.true_course_angle  = 0.0 * Units.degrees 

        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission Specific Unknowns and Residuals 
        # --------------------------------------------------------------------------------------------------------------   
        ones_row                           = self.state.ones_row
        self.state.unknowns.throttle       = ones_row(1) * 0.5
        self.state.residuals.forces        = ones_row(1) * 0.0  
             
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------    
        initialize                         = self.process.initialize
        iterate                            = self.process.iterate 
        initialize.conditions              = Segments.Vertical_Flight.Hover.initialize_conditions
        iterate.residuals.total_forces     = Common.Residuals.vertical_flight_forces        
        return

