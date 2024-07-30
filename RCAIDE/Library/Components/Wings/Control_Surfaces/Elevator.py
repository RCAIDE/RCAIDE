# RCAIDE/Compoments/Wings/Control_Surfaces/Elevator.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports   
from .Control_Surface import Control_Surface 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Attribute
# ----------------------------------------------------------------------------------------------------------------------  
class Elevator(Control_Surface):
    """This class is used to define slats in RCAIDE

    Assumptions:
    None

    Source:
    None

    Args:
    None

    Returns:
    None


    """ 
    def __defaults__(self):
        """This sets the default for slats in RCAIDE.
        
        see Control_Surface().__defaults__ for an explanation of attributes
    
        Assumptions:
        None

        Source:
        None

        Args:
        None

        Returns:
        None

        """ 
        
        self.tag                   = 'elevator'
        self.hinge_fraction        = 0.0
        self.sign_duplicate        = 1.0        
        
        pass 