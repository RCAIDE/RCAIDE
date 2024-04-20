## @ingroup Library-Attributes-Planets
# RCAIDE/Library/Attributes/Planets/Planet.py
# 
#
# Created:  Mar 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------  
#  Imports
# ----------------------------------------------------------------------------------------------------------------------  
 
from RCAIDE.Framework.Core import Data

# ----------------------------------------------------------------------------------------------------------------------  
#  Planet Class
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Attributes-Planets 
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
