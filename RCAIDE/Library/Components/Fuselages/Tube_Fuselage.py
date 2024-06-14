## @ingroup Library-Components-Fuselages
# RCAIDE/Compoments/Fuselages/Tube_Fuselage.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports     
from .Fuselage import Fuselage
 
# ---------------------------------------------------------------------------------------------------------------------- 
#  Tube_Fuselage
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Components-Fuselages 
class Tube_Fuselage(Fuselage):
    """ This is a standard fuselage for a tube and wing aircraft.
    
    Assumptions:
    Conventional fuselage
    
    Source:
    N/A
    """
    
    def __defaults__(self):
        """ This sets the default values for the component to function.
        
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
        self.tag                                    = 'tube_fuselage' 
  