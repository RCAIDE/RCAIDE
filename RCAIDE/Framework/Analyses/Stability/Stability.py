# RCAIDE/Framework/Analyses/Stability/Stability.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports   
from RCAIDE.Framework.Core     import Data
from RCAIDE.Framework.Analyses import Analysis   

# ----------------------------------------------------------------------------------------------------------------------
#  Stability Analysis
# ----------------------------------------------------------------------------------------------------------------------
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
        self.tag      = 'stability'
        self.vehicle  = Data()
        self.settings = Data() 


