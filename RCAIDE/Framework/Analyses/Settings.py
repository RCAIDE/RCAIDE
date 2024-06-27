## @ingroup Framework-Analyses
# RCAIDE/Framework/Analyses/Settings.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
from RCAIDE.Framework.Core import Data

# ----------------------------------------------------------------------------------------------------------------------
# Settings
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Framework-Analyses
class Settings(Data):
    """ The top level settings class 
    """
    def __defaults__(self):
        """This sets the default values and methods for the settings.
        
        Assumptions:
           None

        Source:
           None 
        """             
        self.tag    = 'settings' 
        self.verbose_process = False