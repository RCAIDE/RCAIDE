# RCAIDE/Library/Components/Powertrain/Systems/Hydraulics.py
# 
# Created:  Jan 2026, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports  
from RCAIDE.Library.Components import Component
 
# ----------------------------------------------------------------------------------------------------------------------
#  Hydraulics
# ----------------------------------------------------------------------------------------------------------------------            
class Hydraulics(Component):
    """
    A class representing hydraulic systems and their power requirements. 
    """        
    def __defaults__(self):
        """
        Sets default values for the hydraulic system attributes.
        """                  
        self.tag        = 'hydraulic' 