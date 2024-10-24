# RCAIDE/Framework/Functions/Functions.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports         
from RCAIDE.Framework.Core import Container 

# ----------------------------------------------------------------------------------------------------------------------
#  Functions
# ---------------------------------------------------------------------------------------------------------------------- 
class Missions(Container):
    """Top-level mission class 
    """ 
    
    def __defaults__(self):
        """This sets the default values.
    
            Assumptions:
            None
    
            Source:
            None 
        """         
        self.tag      = 'missions'    

    def append_mission(self,mission):  
        """ Appends a mission to the list of missions 
    
            Assumptions:
                None
    
            Source:
                None
    
            Args:
                self    (dict): Functions data structure of containing process [-]
                mission (dict): mission to be appended                       [-]
    
            Returns:
                None
         """         
        
        self.append(mission)
        return        
    
     