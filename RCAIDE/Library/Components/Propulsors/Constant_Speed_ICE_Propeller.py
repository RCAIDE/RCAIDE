## @ingroup Components-Propulsors 
# RCAIDE/Components/Propulsors/Constant_Speed_ICE_Propeller.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# 
# Created:  Mar 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from .                import Propulsor 

# ----------------------------------------------------------------------
#  Fan Component
# ----------------------------------------------------------------------
## @ingroup Components-Propulsors-Converters
class Constant_Speed_ICE_Propeller(Propulsor):
    """This is an internal engine-propeller propulsor
    
    Assumptions:
    None

    Source:
    None
    """ 
    def __defaults__(self):    
        # setting the default values
        self.tag                          = 'ice_constant_speed_propeller'   
        self.active_fuel_tanks            = None
        self.engine                       = None
        self.propeller                    = None  
          
 
