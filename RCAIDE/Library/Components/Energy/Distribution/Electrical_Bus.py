## @defgroup Library-Compoments-Energy-Networks-Distribution
# RCAIDE/Library/Compoments/Energy/Networks/Distribution/Electrical_Bus.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
import RCAIDE 
from RCAIDE.Library.Components                                import Component
from RCAIDE.Library.Components.Component                      import Container    

# ----------------------------------------------------------------------------------------------------------------------
#  Electrical_Bus
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Compoments-Energy-Networks-Distribution
class Electrical_Bus(Component):
    """Electrical bus component.
    """ 
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """                
        self.tag                           = 'bus' 
        self.batteries                     = Container()
        self.propulsors                    = Container() 
        self.solar_panel                   = None 
        self.avionics                      = RCAIDE.Library.Components.Systems.Avionics()
        self.payload                       = RCAIDE.Library.Components.Payloads.Payload()        
        self.identical_propulsors          = True  
        self.active                        = True
        self.efficiency                    = 1.0
        self.voltage                       = 0.0 
        self.charging_power                = 0.0
         