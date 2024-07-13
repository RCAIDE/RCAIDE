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
    """ RCAIDE.Framework.Analyses.Emissions.Emissions()
    
        The Top Level Emissions Analysis Class
        
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
        self.tag    = 'Emissions'        
  
        self.geometry = Data()
        self.settings = Data()
        
        
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