## @ingroup Library-Attributes-Planets
# RCAIDE/Library/Attributes/Planets/Planet.py
# (c) Copyright 2023 Aerospace Research Community LLC
#
# Created:  Mar 2024, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
 
from RCAIDE.Frameworks.Core import Data
# ----------------------------------------------------------------------
#  Earth Class
# ----------------------------------------------------------------------
## @ingroup Library-Attributes-Planets 
class Planet(Data):
    """Default plantet class 
    
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
        None

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """           
        self.mass              = 0.0  # kg
        self.mean_radius       = 0.0  # m 
