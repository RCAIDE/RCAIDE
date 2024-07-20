# RCAIDE/Compoments/Wings/Main_Wing.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports   
from .Wing import Wing
from RCAIDE.Framework.Core import Container 
from RCAIDE.Library.Components.Wings.Segment import Segment

# ---------------------------------------------------------------------------------------------------------------------- 
#  Main Wing 
# ----------------------------------------------------------------------------------------------------------------------  
class Main_Wing(Wing):
    """Main wing compoment class.
    """
    def __defaults__(self):
        """This sets the default for main wings.
    
        Assumptions:
            None

        Source:
            None 
        """   
        self.tag                 = 'main_wing'
        self.Segments            = Segment_Container()
         
class Segment_Container(Container):
    """ Container for wing segment.
        """    
    
    def append(self,val):
        """Appends the value to the containers. This overrides the basic data class append
    
        Assumptions:
            None

        Source:
            None

        Args:
           self (dict): main wing data structure 
           val  (dict): new data structure 

        Returns:
           None 
        """  
        
        # See if the component exists, if it does modify the name
        keys = self.keys()
        if val.tag in keys:
            string_of_keys = "".join(self.keys())
            n_comps = string_of_keys.count(val.tag)
            val.tag = val.tag + str(n_comps+1)    
            
        Container.append(self,val) 
        
    