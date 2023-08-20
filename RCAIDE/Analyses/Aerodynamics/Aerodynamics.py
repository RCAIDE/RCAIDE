# RCAIDE/Analyses/Aerodynamics/Aerodynamics.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports   
from RCAIDE.Core     import Data
from RCAIDE.Analyses import Analysis  

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Aerodynamics
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Analyses-Aerodynamics
class Aerodynamics(Analysis):
    """This is the base class for aerodynamics analyses. It contains functions
    that are built into the default class.
    
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
        self.tag    = 'aerodynamics'
        
        self.geometry = Data()
        self.settings = Data()
        self.settings.maximum_lift_coefficient = np.inf
        
        
    def evaluate(self,state):
        """The default evaluate function.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        results   <Results class> (empty)

        Properties Used:
        N/A
        """           
        
        results = Data()
        
        return results
    
    def finalize(self):
        """The default finalize function.

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
        
        return     