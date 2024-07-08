# RCAIDE/Library/Components/Propulsors/Propusor.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Library.Components                   import Component 

# ----------------------------------------------------------------------------------------------------------------------
#  Propulsor
# ----------------------------------------------------------------------------------------------------------------------  
class Propulsor(Component):
    """ Default propulsor compoment class. 
    """ 
    def __defaults__(self):
        """ This sets the default values.
    
        Assumptions:
            None

        Source:
           None 
        """          
        self.tag                          = 'propulsor' 
        self.active                       = True 
        
    