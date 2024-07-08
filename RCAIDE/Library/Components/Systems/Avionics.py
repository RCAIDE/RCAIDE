# RCAIDE/Compoments/Systems/Avionics.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports  
from RCAIDE.Library.Components import Component
 
# ----------------------------------------------------------------------------------------------------------------------
#  Avionics
# ----------------------------------------------------------------------------------------------------------------------            
class Avionics(Component):
    """A class representing avionics.
    """        
    def __defaults__(self):
        """This sets the default power draw.

        Assumptions:
            None

        Source:
            None 
        """                 
        self.power_draw = 0.0
        self.tag        = 'avionics'