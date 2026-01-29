# RCAIDE/Library/Components/Powertrain/Systems/Electrical.py
# 
# Created:  Jan 2026, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports  
from RCAIDE.Library.Components import Component
 
# ----------------------------------------------------------------------------------------------------------------------
#  Electrical
# ----------------------------------------------------------------------------------------------------------------------            
class Electrical(Component):
    """
    A class representing electrical control systems and their power requirements. 
    """        
    def __defaults__(self):
        """
        Sets default values for the electrical system attributes.
        """                  
        self.tag        = 'electrical'
        self.power_draw = 0 