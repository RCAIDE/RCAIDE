# RCAIDE/Compoments/Fuselages/Tube_Fuselage.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports     
from .Fuselage import Fuselage
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Tube_Fuselage
# ----------------------------------------------------------------------------------------------------------------------  
class Tube_Fuselage(Fuselage):
    """ This is a standard fuselage for a tube and wing aircraft.
    
    Assumptions:
       conventional fuselage properties
    
    Source:
       None
    """
    
    def __defaults__(self):
        """ This sets the default values for the component to function.
        
        Assumptions:
            None
    
        Source:
            None 
        """      
        self.tag                                    = 'tube_fuselage' 
  