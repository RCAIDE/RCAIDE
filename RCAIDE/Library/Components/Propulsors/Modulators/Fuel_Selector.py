# RCAIDE/Library/Components/Propulsors/Modulators/Fuel_Selector.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Library.Components import Component
 
# ----------------------------------------------------------------------------------------------------------------------
#  Fuel_Selector
# ----------------------------------------------------------------------------------------------------------------------  
class Fuel_Selector(Component):
    
    def __defaults__(self):
        """ This sets the default values.
    
        Assumptions:
            None

        Source:
            None

        Args:
           self 
        """        

        self.tag              = 'fuel_selector'  
        self.efficiency       = 0.0       
     