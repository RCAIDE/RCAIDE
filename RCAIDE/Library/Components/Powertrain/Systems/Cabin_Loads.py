# RCAIDE/Library/Components/Powertrain/Systems/Cabin_Loads.py
# 
# Created:  May 2026, M. Clarke, S. Sharma

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports  
from RCAIDE.Library.Methods.Powertrain.Systems import append_ice_protection_conditions

from .Systems import Systems
from RCAIDE.Library.Methods.Powertrain.Systems.append_cabin_loads_conditions import append_cabin_loads_conditions
 
# ----------------------------------------------------------------------------------------------------------------------
#  Cabin_Loads
# ----------------------------------------------------------------------------------------------------------------------            
class Cabin_Loads(Systems):
    """
    A class representing cabin loads and their power requirements. 
    """        
    def __defaults__(self):
        """
        Sets default values for the cabin loads system attributes.
        """                  
        self.tag        = 'cabin_loads' 
        
    def append_operating_conditions(self, segment, bus): 
        """
        Adds operating conditions for the cabin loads system to a mission segment.

        Parameters
        ----------
        segment : Data
            Mission segment to which conditions are being added
        bus : Data
            Electrical bus supplying power to the avionics
        """
        append_cabin_loads_conditions(self, segment, bus)
        return         
    
    