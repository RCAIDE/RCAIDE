## @ingroup Framework-Analyses-Stability
# RCAIDE/Framework/Analyses/Stability/Stability.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports   
from RCAIDE.Framework.Core     import Data
from RCAIDE.Framework.Analyses import Analysis   

# ----------------------------------------------------------------------
#  Analysis
# ----------------------------------------------------------------------

## @ingroup Framework-Analyses-Stability
class Stability(Analysis):
    """This is the base class for stability analyses. It contains functions
    that are built into the default class. 
    """
     
    def __defaults__(self):
        """This sets the default values and methods for the stability analysis.         

        Assumptions:
            None

        Source:
            None
        """   
        self.tag    = 'stability'
        self.geometry = Data()
        self.settings = Data() 


