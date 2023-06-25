## @ingroup Analyses-Planets
# Planet.py
#
# Created:  
# Modified: Feb 2016, Andrew Wendorff

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from Legacy.trunk.S.Core import Data
from Legacy.trunk.S.Analyses import Analysis

# ----------------------------------------------------------------------
#  Analysis
# ----------------------------------------------------------------------

## @ingroup Analyses-Planets
class Planet(Analysis):
    """ SUAVE.Analyses.Planet()
    """
    
    def __defaults__(self):
        
        """This sets the default values and methods for the analysis.
    
            Assumptions:
            Planet is Earth.
    
            Source:
            N/A
    
            Inputs:
            None
    
            Outputs:
            None
    
            Properties Used:
            N/A
            """                  
        
        
        self.tag    = 'planet'
        self.features = Data()
        self.settings = Data()
        
        from Legacy.trunk.S.Attributes.Planets.Earth import Earth
        self.features = Earth()
        
        
        