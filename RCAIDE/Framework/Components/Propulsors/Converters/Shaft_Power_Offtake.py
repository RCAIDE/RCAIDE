# RCAIDE/Library/Components/Propulsors/Converters/Shaft_Power_Offtake.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Feb 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from RCAIDE.Framework.Components import Component

# ---------------------------------------------------------------------------------------------------------------------- 
# Shaft_Power_Offtake
# ---------------------------------------------------------------------------------------------------------------------- 
class Shaft_Power_Offtake(Component):
    """This is a component representing the power draw from the shaft. 
    """ 
    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
            None

        Source:
            None 
        """          
        self.power_draw            = 0.0
        self.reference_temperature = 288.15
        self.reference_pressure    = 1.01325 * 10 ** 5 
