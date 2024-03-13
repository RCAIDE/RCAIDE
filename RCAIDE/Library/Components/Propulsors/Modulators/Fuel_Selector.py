## @ingroup Components-Propulsors-Modulators
# RCAIDE/Library/Components/Propulsors/Modulators/Fuel_Selector.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Library.Components import Component
 
# ----------------------------------------------------------------------------------------------------------------------
#  Fuel_Selector
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Distributors
class Fuel_Selector(Component):
    
    def __defaults__(self):
        """ This sets the default values.
    
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

        self.tag              = 'fuel_selector'  
        self.efficiency       = 0.0       
     