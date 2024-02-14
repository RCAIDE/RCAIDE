## @ingroup Energy-Propulsion-Converters
# RCAIDE/Energy/Propulsion/Converters/Fan.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from .                import Propulsor 

# ----------------------------------------------------------------------
#  Fan Component
# ----------------------------------------------------------------------
## @ingroup Energy-Propulsion-Converters
class Electric_Rotor(Propulsor):
    """This is a   
    
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
      
    def compute_thrust(self,conditions,throttle = 1.0): 
        
        return 
          
 
