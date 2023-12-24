## @ingroup Energy-Propulsion-Modulators
# RCAIDE/Energy/Propulsion/Modulators/Fuel_Selector.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Energy.Energy_Component import Energy_Component
 
# ----------------------------------------------------------------------------------------------------------------------
#  Fuel_Selector
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Distributors
class Fuel_Selector(Energy_Component):
    
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
     