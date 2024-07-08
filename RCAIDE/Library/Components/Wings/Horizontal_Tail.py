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
class Horizontal_Tail(Wing):
    """ Horizontal tail compoment class 
        """ 

    def __defaults__(self):
        """This sets the default for horizontal tails.
    
        Assumptions:
            None

        Source:
            None 
        """ 
        self.tag = 'horizontal_stabilizer'