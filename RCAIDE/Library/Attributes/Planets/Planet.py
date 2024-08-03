# RCAIDE/Library/Attributes/Planets/Planet.py
# (c) Copyright 2023 Aerospace Research Community LLC
#
# Created: Mar 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------  
#  Imports
# ----------------------------------------------------------------------------------------------------------------------  
 
from RCAIDE.Reference.Core import Data

# ----------------------------------------------------------------------------------------------------------------------  
#  Planet Class
# ----------------------------------------------------------------------------------------------------------------------   
class Planet(Data):
    """Default planet class 
    """
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """           
        self.mass              = 0.0  # kg
        self.mean_radius       = 0.0  # m 
