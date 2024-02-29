## @ingroup Energy-Propulsors-Shaft_Power_Offtake
# RCAIDE/Energy/Propulsors/Converters/Shaft_Power_Offtake.py
# 
# 
# Created:  Feb 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from RCAIDE.Energy.Energy_Component                      import Energy_Component  

# ---------------------------------------------------------------------------------------------------------------------- 
# Shaft_Power_Offtake
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Propulsors-Converters 
class Shaft_Power_Offtake(Energy_Component):
    """This is a component representing the power draw from the shaft.
    
    Assumptions:
    None

    Source:
    None
    """ 
    def __defaults__(self):
        """This sets the default values for the component to function.

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
        self.power_draw            = 0.0
        self.reference_temperature = 288.15
        self.reference_pressure    = 1.01325 * 10 ** 5 
