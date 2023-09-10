## @ingroup Attributes-Propellants 
# RCAIDE/Attributes/Aviation_Gasoline.py
# (c) Copyright 2023 Aerospace Research Community LLC 
# 
# Created:  Sep 2023, M. Clarke
# Modified: 
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
from .Propellant import Propellant 

# ----------------------------------------------------------------------------------------------------------------------
#  Aviation_Gasoline  
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Attributes-Propellants
class Aviation_Gasoline(Propellant):
    """Contains density and specific energy values for this propellant
    
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
        Values commonly available

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """    
        self.tag             ='Aviation_Gasoline'
        self.density         = 721.0            # kg/m^3
        self.specific_energy = 43.71e6          # J/kg
        
