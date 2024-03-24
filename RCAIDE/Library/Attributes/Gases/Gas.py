## @ingroup Library-Attributes-Gases
# RCAIDE/Library/Attributes/Gases/Gas.py
# (c) Copyright 2023 Aerospace Research Community LLC
#
# Created:  Mar 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------  
#  Imports
# ----------------------------------------------------------------------------------------------------------------------  

from RCAIDE.Framework.Core import Data 

# ----------------------------------------------------------------------------------------------------------------------  
#  Gas Class
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Attributes-Gases 
class Gas(Data):
    """Default class for all gases 

    Assumptions:
    None

    Source:
    None
    """

    def __defaults__(self):
        """This sets the default values.
    
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
        self.tag                   ='gas'
        self.molecular_mass        = 0.0    
        self.gas_specific_constant = 0.0              
        self.composition           = Data()
        self.composition.gas       = 1.0
