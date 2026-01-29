# RCAIDE/Library/Components/Powertrain/Systems/Environmental_Controls.py
# 
# Created:  Jan 2026, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports  
from RCAIDE.Library.Components import Component
 
# ----------------------------------------------------------------------------------------------------------------------
#  Environmental_Controls
# ----------------------------------------------------------------------------------------------------------------------            
class Environmental_Controls(Component):
    """
    A class representing environmental control systems and their power requirements. 
    """        
    def __defaults__(self):
        """
        Sets default values for the environmental control system attributes.
        """                  
        self.tag        = 'environmental_control' 