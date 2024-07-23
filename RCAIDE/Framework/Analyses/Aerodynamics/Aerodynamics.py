# RCAIDE/Framework/Analyses/Aerodynamics/Aerodynamics.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports   
from RCAIDE.Framework.Core     import Data
from RCAIDE.Framework.Analyses import Analysis  

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Aerodynamics
# ---------------------------------------------------------------------------------------------------------------------- 
class Aerodynamics(Analysis):
    """This is the base class for aerodynamics analyses. 
    """
    def __defaults__(self):
        """This sets the default values and methods for the analysis.

        Assumptions:
            None

        Source:
            None 
        """           
        self.tag                               = 'aerodynamics'  
        self.geometry                          = Data()
        self.settings                          = Data()
        self.settings.maximum_lift_coefficient = np.inf