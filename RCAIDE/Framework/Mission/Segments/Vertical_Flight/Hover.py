# RCAIDE/Framework/Mission/Segments/Vertical_Flight/Hover.py
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
#  Hover
# ----------------------------------------------------------------------------------------------------------------------
class Hover(Evaluate):
    """ A stationary hover for VTOL aircraft. No aerodynamic drag and lift are used, since there is no velocity. 
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
        
        self.altitude           = None
        self.time               = 1.0 * Units.seconds
        self.true_course        = 0.0 * Units.degrees            
             
        # -------------------------------------------------------------------------------------------------------------- 
        #  Mission specific processes 
        # --------------------------------------------------------------------------------------------------------------    
        initialize                         = self.process.initialize
        iterate                            = self.process.iterate 
        initialize.conditions              = Segments.Vertical_Flight.Hover.initialize_conditions
        iterate.residuals.flight_dynamics  = Common.Residuals.flight_dynamics
        return

