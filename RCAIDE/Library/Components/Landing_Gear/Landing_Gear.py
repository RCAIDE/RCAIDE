## @ingroup Library-Compoments-Landing_Gear
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
## @ingroup Library-Compoments-Landing_Gear
class Landing_Gear(Component):
    """ Landing gear default class 
        
        Assumptions:
        None
        
        Source:
        N/A
    
        """

    def __defaults__(self):
        """ This sets the default values for the component attributes.
        
                Assumptions:
                None
                
                Source:
                N/A
                
                Args:
                None
                
                Returns:
                None
                
                Properties Used:
                N/A
        """
       
        self.tag = 'landing_gear'
     