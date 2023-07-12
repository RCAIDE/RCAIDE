# RCAIDE/Analyses/Settings.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# Legacy imports   
from Legacy.trunk.S.Core import Data

# ----------------------------------------------------------------------------------------------------------------------
# ANALYSIS
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Analyses
class Settings(Data):
    """ RCAIDE.Analyses.Settings()
    
        The Top Level Settings Class
        
            Assumptions:
            None
            
            Source:
            N/A
    """
    def __defaults__(self):
        """This sets the default values and methods for the settings.
        
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
        self.tag    = 'settings'
        
        self.verbose_process = False