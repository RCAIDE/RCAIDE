## @ingroup Components-Energy-Converters
# Shaft_Power_Off_Take.py
#
# Created:  Jun 2016, L. Kulik

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# SUAVE imports
from Legacy.trunk.S.Components.Energy.Energy_Component import Energy_Component

# package imports
import numpy as np

# ----------------------------------------------------------------------
#  Shaft Power component
# ----------------------------------------------------------------------
## @ingroup Components-Energy-Converters
class Shaft_Power_Off_Take(Energy_Component):
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
        self.power_draw = 0.0
        self.reference_temperature = 288.15
        self.reference_pressure = 1.01325 * 10 ** 5 
