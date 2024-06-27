## @ingroup Library-Compoments-Landing_Gear
# RCAIDE/Library/Compoments/Landing_Gear/Nose_Landing_Gear.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

 # RCAIDE imports 
from .Landing_Gear import Landing_Gear

# ----------------------------------------------------------------------------------------------------------------------
#  Nose_Landing_Gear
# ----------------------------------------------------------------------------------------------------------------------    
## @ingroup Library-Compoments-Landing_Gear 
class Nose_Landing_Gear(Landing_Gear):
    """ Nose landing gear compoment class.
    """

    def __defaults__(self): 
        
        """ This sets the default values for the component attributes.
        
        Assumptions:
            None
        
        Source:
            None 
        """
        self.tag           = 'nose_gear'
        self.tire_diameter = 0.    
        self.strut_length  = 0.    
        self.units         = 0. # number of nose landing gear    
        self.wheels        = 0. # number of wheels on the nose landing gear 