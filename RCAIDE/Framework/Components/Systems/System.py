# RCAIDE/Compoments/Systems/System.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports  
from RCAIDE.Framework.Components import Component
 
# ----------------------------------------------------------------------------------------------------------------------
# System
# ----------------------------------------------------------------------------------------------------------------------    
class System(Component):
    """A class representing an aircraft system/systems. 
    """  
    def __defaults__(self): 
        """ This sets the default values for the system.
        
        Assumptions:
            None
        
        Source:
            None 
        """     
        self.tag             = 'system'
        self.origin          = [[0.0,0.0,0.0]]
        self.control         = None
        self.accessories     = None 