## @defgroup Energy-Networks-Distribution
# RCAIDE/Energy/Networks/Distribution/Electrical_Bus.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
import RCAIDE 
from RCAIDE.Energy.Energy_Component                   import Energy_Component
from RCAIDE.Components.Component                      import Container    

# ----------------------------------------------------------------------------------------------------------------------
#  Electrical_Bus
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Networks-Distribution
class Electrical_Bus(Energy_Component):
    """  This controls the flow of energy into and from a battery-powered nework 
    
        Assumptions:
        None
        
        Source:
        None
    """
    
    
    def __defaults__(self):
        """ This sets the default values.
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:
            None
    
            Outputs:
            None
    
            Properties Used:
            None
        """          
        self.tag                           = 'bus' 
        self.batteries                     = Container()
        self.propulsors                    = Container() 
        self.solar_panel                   = None 
        self.avionics                      = RCAIDE.Energy.Peripherals.Avionics()
        self.payload                       = RCAIDE.Energy.Peripherals.Payload()        
        self.identical_propulsors          = True  
        self.active                        = True
        self.efficiency                    = 1.0
        self.voltage                       = 0.0 
        self.charging_power                = 0.0
         