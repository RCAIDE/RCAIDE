# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Core import Data 
from RCAIDE.Attributes.Coolants.Glycol_Water import Glycol_Water
from RCAIDE.Energy.Energy_Component            import Energy_Component 

# ----------------------------------------------------------------------------------------------------------------------
# Conjugate_Heat_Removal_System  
# ----------------------------------------------------------------------------------------------------------------------
class Conjugate_HRS(Energy_Component):
    
    def __defaults__(self):  
        self.tag                          = 'Conjugate_Heat_Removal_System' 
        self.heat_transfer_efficiency     = 1.0
        
        self.coolant                      = Glycol_Water()
        self.channel_thickness            = 0.5        # Thickness of the Chanel through which condcution occurs (Replace with funciton)
        self.channel_width                = 0.5        # width of the channel (Replace with function)
        self.channel_height               = 0.3        # height of the channel (Replace with function)
        self.channel_contact_angle        = 47.5       # Contact Arc angle in degrees    
        self.channel_thermal_conductivity = 237       # Conductivity of the Channel (Replace with function)
    
 