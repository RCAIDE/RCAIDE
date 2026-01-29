# RCAIDE/Library/Components/Powertrain/Systems/Environmental_Controls.py
# 
# Created:  Jan 2026, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports  
from RCAIDE.Library.Components.Powertrain.Converters import Turboelectric_Generator
 
# ----------------------------------------------------------------------
# Auxillary_Power_Unit
# ----------------------------------------------------------------------
class Auxillary_Power_Unit(Turboelectric_Generator): 
    """
    A class representing auxillary power unit and their power requirements. 
    """        
    def __defaults__(self):
        """
        Sets default values for the auxillary power unit attributes.
        """                  
        self.tag        = 'apu'
