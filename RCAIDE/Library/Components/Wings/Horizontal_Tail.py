## @ingroup Library-Components-Wings
# RCAIDE/Compoments/Wings/Horizontal_Tail.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports   
from .Wing import Wing 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Main Wing 
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Components-Wings   
class Horizontal_Tail(Wing):
    """ This is the horizontal stabilizer class  
    
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
        """This sets the default for horizontal tails.
    
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
        self.tag = 'horizontal_stabilizer'