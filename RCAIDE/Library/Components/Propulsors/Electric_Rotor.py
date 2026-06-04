# RCAIDE/Library/Components/Propulsors/Electric_Rotor.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# 
# Created: Mar 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports   
from .                import Propulsor 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Electric_Rotor Component
# ---------------------------------------------------------------------------------------------------------------------- 
class Electric_Rotor(Propulsor):
    """This is a electric motor-rotor propulsor  
    """ 
    def __defaults__(self):    
        # setting the default values
        self.tag                          = 'electric_rotor'   
        self.active_batteries             = None
        self.motor                        = None
        self.rotor                        = None 
        self.electronic_speed_controller  = None  
          
 
