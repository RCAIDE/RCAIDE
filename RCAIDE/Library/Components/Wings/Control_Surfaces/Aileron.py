## @ingroup Library-Components-Wings-Control_Surfaces
# RCAIDE/Compoments/Wings/Control_Surfaces/Aileron.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports   
from .Control_Surface import Control_Surface 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Attribute
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Components-Wings-Control_Surfaces
class Aileron(Control_Surface):
    """This class is used to define slats in RCAIDE

    Assumptions:
    None

    Source:
    N/A

    Inputs:
    None

    Outputs:
    None

    Properties Used:
    N/A
    """ 
    def __defaults__(self):
        """This sets the default for slats in RCAIDE.
        
        see Control_Surface().__defaults__ for an explanation of attributes
    
        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """ 
        
        self.tag                   = 'aileron'  
        self.hinge_fraction        = 0.0
        self.sign_duplicate        = -1.0
        
        pass 