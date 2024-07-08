# RCAIDE/Library/Compoments/Configs/Config.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Framework.Core    import Diffed_Data
from RCAIDE.Vehicle          import Vehicle  

# ----------------------------------------------------------------------------------------------------------------------
#  Config
# ----------------------------------------------------------------------------------------------------------------------   
class Config(Diffed_Data,Vehicle):
    """ The top level configuration class.
    """ 
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """     
        self.tag    = 'config'
        self._base  = Vehicle()
        self._diff  = Vehicle()
