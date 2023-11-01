## @ingroup Analyses-Aerodynamics-Airfoils
# Wing_Airfoil.py
#
# Created:  Oct 2023, Racheal M. Erhard
# Modified: 

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
from . import Airfoil


# ----------------------------------------------------------------------
#  Analysis
# ----------------------------------------------------------------------
## @ingroup Analyses-Aerodynamics-Airfoils
class Wing_Airfoil(Airfoil):
    """This is the class for airfoil analyses. It contains functions
    for wing airfoil analysis, specifically for use in wing analysis.
    
    Assumptions:
    None
    
    Source:
    N/A
    """
    def __defaults__(self):
        """This sets the default values and methods for the wing airfoil analysis.

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
        self.tag = 'Wing_Airfoil_Analysis'
        
        # Settings default to no polar analysis to run
        self.settings.use_panel_method = False      
        self.settings.use_polar_import = False      
        