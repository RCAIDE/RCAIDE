# RCAIDE/Compoments/Fuselages/Blended_Wing_Body_Fuselage.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports    
from .Fuselage import Fuselage

# ---------------------------------------------------------------------------------------------------------------------- 
#  Blended_Wing_Body_Fuselage
# ----------------------------------------------------------------------------------------------------------------------  
class Blended_Wing_Body_Fuselage(Fuselage):
    """ This is a blended wing body fuselage class  
    """
    
    def __defaults__(self):
        """ This sets the default values for the component to function.
        
        Assumptions:
            None
    
        Source:
            None 
        """       
        self.tag                   = 'bwb_fuselage'
        self.aft_centerbody_area   = 0.0
        self.aft_centerbody_taper  = 0.0
        self.cabin_area            = 0.0   