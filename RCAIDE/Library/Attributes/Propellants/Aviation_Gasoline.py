# RCAIDE/Library/Attributes/Aviation_Gasoline.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Sep 2023, RCAIDE Team
# Modified:
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
from .Propellant import Propellant 

# ----------------------------------------------------------------------------------------------------------------------
#  Aviation_Gasoline  
# ----------------------------------------------------------------------------------------------------------------------  
class Aviation_Gasoline(Propellant):
    """Aviation gasoline class
    """

    def __defaults__(self):
        """This sets the default values. 
    
        Assumptions:
            None
        
        Source:
            None
        """    
        self.tag             ='Aviation_Gasoline'
        self.density         = 721.0            # kg/m^3
        self.specific_energy = 43.71e6          # J/kg
        
