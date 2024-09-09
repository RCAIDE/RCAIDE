# RCAIDE/Library/Components/Propulsors/Constant_Speed_ICE_Propeller.py
# (c) Copyright 2023 Aerospace Research Community LLC
#  
# Created: Mar 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from .                import Propulsor 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Constant_Speed_ICE_Propeller
# ---------------------------------------------------------------------------------------------------------------------- 
class Constant_Speed_ICE_Propeller(Propulsor):
    """This is an internal engine-propeller propulsor 
    """ 
    def __defaults__(self):    
        # setting the default values
        self.tag                          = 'ice_constant_speed_propeller'   
        self.active_fuel_tanks            = None
        self.engine                       = None
        self.propeller                    = None  
          
 
