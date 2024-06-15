## @ingroup Framework-Mission-Segments-Conditions 
# RCAIDE/Framework/Mission/Segments/Conditions/Residuals.py
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

## @ingroup Framework-Mission-Segments-Conditions
class Residuals(Conditions):
    """ Creates the data structure for the residuals that solved in a mission.
    """    
    
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
    
        Source:
            None 
        """           
        self.tag      = 'residuals'