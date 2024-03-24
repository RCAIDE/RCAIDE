## @ingroup Library-Attributes-Atmospheres
# RCAIDE/Library/Attributes/Atmospheres/Atmosphere.py
# (c) Copyright 2023 Aerospace Research Community LLC
#
# Created:  Mar 2024, M. Clarke

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 
 
from RCAIDE.Framework.Core import Data

# ---------------------------------------------------------------------------------------------------------------------- 
#  Industrial_Costs Class
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Attributes-Atmospheres 
class Atmosphere(Data):
    """Default atmospheric class 
    
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
        self.tag = 'Constant-property atmosphere'
        self.composition           = Data()
        self.composition.gas       = 1.0
