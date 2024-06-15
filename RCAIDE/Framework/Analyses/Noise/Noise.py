## @ingroup Analyses-Noise
# RCAIDE/Framework/Analyses/Noise/Noise.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

from RCAIDE.Framework.Core     import Data
from RCAIDE.Framework.Analyses import Analysis

# ----------------------------------------------------------------------
#  Noise
# ----------------------------------------------------------------------
## @ingroup Analyses-Noise
class Noise(Analysis):
    """This is the base class for noise analyses. It contains functions
    that are built into the default class. 
    """
    def __defaults__(self):
        """This sets the default values and methods for the noise analysis.
    
        Assumptions:
            None

        Source:
            None 
            """                   
        self.tag      = 'Noise'         
        self.geometry = Data()
        self.settings = Data()
         