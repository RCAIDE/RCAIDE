# RCAIDE/Library/Attributes/Atmospheres/Atmosphere.py
# (c) Copyright 2023 Aerospace Research Community LLC
#
# Created: Mar 2024, RCAIDE Team

# ---------------------------------------------------------------------------------------------------------------------- 
#  Imports
# ---------------------------------------------------------------------------------------------------------------------- 
 
from RCAIDE.Reference.Core import Data

# ---------------------------------------------------------------------------------------------------------------------- 
#  Industrial_Costs Class
# ----------------------------------------------------------------------------------------------------------------------   
class Atmosphere(Data):
    """Default atmosphere class 
    """

    def __defaults__(self):
        """This sets the default values. 
    
        Assumptions:
            None
        
        Source:
            None 
        """          
        self.tag = 'Constant-property atmosphere'
        self.composition           = Data()
        self.composition.gas       = 1.0
