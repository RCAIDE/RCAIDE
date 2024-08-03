# RCAIDE/Framework/Functions/Segments/Conditions/Residuals.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Residuals
# ----------------------------------------------------------------------------------------------------------------------
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