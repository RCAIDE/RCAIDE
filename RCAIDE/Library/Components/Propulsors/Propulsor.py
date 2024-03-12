## @ingroup Components-Propulsors
# RCAIDE/Components/Propulsors/Propusor.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Components                   import Component 

# ----------------------------------------------------------------------------------------------------------------------
#  Propusor
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Distributors
class Propulsor(Component):
    """  This controls the flow of energy into and from a battery-powered nework 
    
        Assumptions:
        None
        
        Source:
        None
    """
    
    
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
        self.tag                          = 'propulsor' 
        self.active                       = True 
        
    