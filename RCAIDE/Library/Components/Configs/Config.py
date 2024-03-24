## @defgroup Library-Compoments-Configs
# RCAIDE/Library/Compoments/Configs/Config.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Framework.Core    import Diffed_Data
from RCAIDE.Vehicle          import Vehicle  

# ----------------------------------------------------------------------------------------------------------------------
#  Config
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Components-Configs
class Config(Diffed_Data,Vehicle):
    """ The Top Level Configuration Class
        
            Assumptions:
            None
            
            Source:
            N/A
    """
    
    def __defaults__(self):
        """ This sets the default values for the configuration.
        
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
        self.tag    = 'config'
        self._base  = Vehicle()
        self._diff  = Vehicle()
