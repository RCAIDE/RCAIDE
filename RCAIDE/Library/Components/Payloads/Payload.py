## @ingroup Library-Compoments-Payload
# RCAIDE/Compoments/Payload/Payload.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports  
from RCAIDE.Library.Components import Component
 
# ----------------------------------------------------------------------------------------------------------------------
#  Payload
# ----------------------------------------------------------------------------------------------------------------------           
## @ingroup Library-Compoments-Payload
class Payload(Component):
    """Payload component class. 
    """          
    def __defaults__(self):
        """This sets the default power draw.

        Assumptions:
            None

        Source:
            None 
        """            
        self.power_draw = 0.0