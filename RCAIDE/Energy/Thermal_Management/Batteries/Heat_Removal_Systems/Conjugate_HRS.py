# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
from RCAIDE.Core import Data , Units
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
        self.coolant_flow_rate            = 0.001
        self.channel_side_thickness       = 0.5      # Thickness of the Chanel through which condcution occurs 
        self.channel_top_thickness        = 0.5      # Thickness of Channel on the top where no conduction occurs
        self.channel_width                = 1.5      # width of the channel 
        self.channel_height               = 0.3      # height of the channel 
        self.channel_contact_angle        = 47.5     # Contact Arc angle in degrees    
        self.channel_thermal_conductivity = 237      # Conductivity of the Channel
        self.channel_density              = 2710     # Denisty of the Channel
    
 