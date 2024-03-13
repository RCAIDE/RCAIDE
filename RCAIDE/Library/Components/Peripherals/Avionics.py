## @ingroup Library-Compoments-Peripherals
# RCAIDE/Compoments/Peripherals/Avionics.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports  
from RCAIDE.Library.Components import Component
 
# ----------------------------------------------------------------------------------------------------------------------
#  Avionics
# ----------------------------------------------------------------------------------------------------------------------           
## @ingroup Energy-Peripherals 
class Avionics(Component):
    """A class representing avionics.
    
    Assumptions:
    None
    
    Source:
    N/A
    """        
    def __defaults__(self):
        """This sets the default power draw.

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
        self.power_draw = 0.0
        self.tag        = 'avionics'
        
    def power(self):
        """This gives the power draw from avionics.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        self.outputs.power_draw          [Watts]
                                           
        Properties Used:
        self.power_draw    
        """                 
        self.inputs.power = self.power_draw
        
        return self.power_draw