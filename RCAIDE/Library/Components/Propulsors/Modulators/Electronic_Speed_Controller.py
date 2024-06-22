## @ingroup Components-Propulsors-Modulators
# RCAIDE/Library/Components/Propulsors/Modulators/Electronic_Speed_Controller.py
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
#  Electronic Speed Controller Class
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Distributors
class Electronic_Speed_Controller(Component):
    
    def __defaults__(self):
        """ This sets the default values.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Args:
            None
    
            Returns:
            None
    
            Properties Used:
            None
            """         

        self.tag              = 'electronic_speed_controller'  
        self.efficiency       = 0.0       