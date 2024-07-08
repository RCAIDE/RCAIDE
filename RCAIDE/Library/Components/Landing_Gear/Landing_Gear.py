# RCAIDE/Library/Compoments/Landing_Gear/Landing_Gear.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

 # RCAIDE imports 
from RCAIDE.Library.Components    import Component   

# ----------------------------------------------------------------------------------------------------------------------
#  Landing_Gear
# ----------------------------------------------------------------------------------------------------------------------   
class Landing_Gear(Component):
    """ Landing gear default class  
        """

    def __defaults__(self):
        """ This sets the default values for the component attributes.
        
        Assumptions:
            None
        
        Source:
            None 
        """ 
        self.tag = 'landing_gear'
     