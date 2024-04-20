## @ingroup Components-Propulsors-Electric_Rotor
# RCAIDE/Library/Components/Propulsors/Electric_Rotor.py
# 
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
class Electric_Rotor(Propulsor):
    """This is a electric motor-rotor propulsor 
    
    Assumptions:
    None

    Source:
    None
    """ 
    def __defaults__(self):    
        # setting the default values
        self.tag                          = 'electric_rotor'   
        self.active_batteries             = None
        self.motor                        = None
        self.rotor                        = None 
        self.electronic_speed_controller  = None  
          
 
