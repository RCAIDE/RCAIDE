## @ingroup Energy-Peripherals
# RCAIDE/Energy/Peripherals/Avionics.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports  
from RCAIDE.Energy.Energy_Component import Energy_Component
 
# ----------------------------------------------------------------------------------------------------------------------
#  Avionics
# ----------------------------------------------------------------------------------------------------------------------           
## @ingroup Energy-Peripherals 
class Avionics(Energy_Component):
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