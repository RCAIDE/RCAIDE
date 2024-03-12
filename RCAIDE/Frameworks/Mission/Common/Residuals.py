## @ingroup Frameworks-Mission-Common
# RCAIDE/Frameworks/Mission/Common/Residuals.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Residuals
# ----------------------------------------------------------------------------------------------------------------------

## @ingroup Frameworks-Mission-Common
class Residuals(Conditions):
    """ Creates the data structure for the residuals that solved in a mission
    
        Assumptions:
        None
        
        Source:
        None
    """    
    
    def __defaults__(self):
        """This sets the default values.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            None
    
            Outputs:
            None
    
            Properties Used:
            None
        """           
        self.tag      = 'residuals'