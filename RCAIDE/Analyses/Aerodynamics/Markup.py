## @ingroup Analyses-Aerodynamics
# RCAIDE/Analyses/Aerodynamics/Process_Geometry.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Core     import Data
from RCAIDE.Analyses import Process
from .Aerodynamics   import Aerodynamics 

# ----------------------------------------------------------------------------------------------------------------------
#  Analysis
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Analyses-Aerodynamics
class Markup(Aerodynamics):
    """This is an intermediate class for aerodynamic analyses.

    Assumptions:
    None

    Source:
    N/A
    """  
    def __defaults__(self):
        """This sets the default values and methods for the analysis.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """           
        self.tag                                      = 'aerodynamics_markup' 
        self.geometry                                 = Data()
        self.settings.maximum_lift_coefficient_factor = 1.0        
        self.settings.lift_to_drag_adjustment         = 0.  
        self.process                                  = Process()
        self.process.initialize                       = Process()
        self.process.compute                          = Process()
        
        
    def evaluate(self,state):
        """The default evaluate function.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        results   <RCAIDE data class>

        Properties Used:
        self.settings
        self.geometry
        """          
        settings = self.settings
        geometry = self.geometry
        
        results = self.process.compute(state,settings,geometry)
        
        return results
        
    def initialize(self):
        """The default finalize function. Calls the initialize process.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """            
        self.process.initialize(self)  