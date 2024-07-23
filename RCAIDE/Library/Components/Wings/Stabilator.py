# RCAIDE/Compoments/Wings/Stabilator.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports   
from .Horizontal_Tail    import Horizontal_Tail
from .All_Moving_Surface import All_Moving_Surface

# ---------------------------------------------------------------------------------------------------------------------- 
#  Stabilator
# ----------------------------------------------------------------------------------------------------------------------     
class Stabilator(Horizontal_Tail, All_Moving_Surface):
    """ This class is used to define stabilatorsE. It 
    inherits from both Horizontal_Tail and All_Moving_Surface 
        """ 

    def __defaults__(self):
        """This sets the default for stabilators.
    
        Assumptions:
            None

        Source:
            See All_Moving_Surface().__defaults__ and Wing().__defaults__ for 
            an explanation of attributes
        """ 
        self.tag                = 'stabilator'
        self.sign_duplicate     = 1.0
