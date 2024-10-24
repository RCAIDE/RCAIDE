# RCAIDE/Library/Compoments/Landing_Gear/Main_Landing_Gear.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Mar 2024, RCAIDE Team
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

 # RCAIDE imports 
from .Landing_Gear import Landing_Gear

# ----------------------------------------------------------------------------------------------------------------------
# Main_Landing_Gear
# ----------------------------------------------------------------------------------------------------------------------     
class Main_Landing_Gear(Landing_Gear):
    """Main landing gear compoment class   
    """

    def __defaults__(self):
        """ This sets the default values for the component attributes.
        
        Assumptions:
            None
        
        Source:
            None 
        """
        self.tag           = 'main_gear'
        self.units         = 0. # number of main landing gear units        
        self.strut_length  = 0.
        self.tire_diameter = 0. 
        self.wheels        = 0. # number of wheels on the main landing gear 