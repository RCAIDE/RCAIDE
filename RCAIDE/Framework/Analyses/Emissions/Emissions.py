## @ingroup Analyses-Emissions
# RCAIDE/Framework/Analyses/Emissions/Emissions.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

from RCAIDE.Framework.Core import Data
from RCAIDE.Framework.Analyses import Analysis

# ----------------------------------------------------------------------
#  Emissions
# ----------------------------------------------------------------------
## @ingroup Analyses-Emissions
class Emissions(Analysis):
    """ The Top Level Emissions Analysis Class 
    """
    def __defaults__(self):
        """This sets the default values and methods for the analysis.
    
            Assumptions:
            None
    
            Source:
            None 
            """                   
        self.tag    = 'Emissions'        
  
        self.geometry = Data()
        self.settings = Data()
        
        
    def evaluate(self,state):
        """The default evaluate function.

        Assumptions:
        None

        Source:
        None 

        Inputs:
        self   - emissions analyses 
        state  - flight conditions 

        Outputs:
        results  
        """         
        results = Data()
        
        return results 