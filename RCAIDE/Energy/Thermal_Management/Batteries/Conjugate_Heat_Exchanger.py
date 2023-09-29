## @ingroup Energy-Thermal_Management-Batteries
# RCAIDE/Energy/Thermal_Management/Batteries/Conjugate_Heat_Exchanger.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
from RCAIDE.Core import Data
from RCAIDE.Energy.Energy_Component import Energy_Component 
#from RCAIDE.Methods.Thermal_Management.Batteries.Atmospheric_Air_Convection_Cooling.direct_convection_model import compute_net_convected_heat 
from RCAIDE.Attributes.Gases import Air

# ----------------------------------------------------------------------------------------------------------------------
#  Atmospheric_Air_Convection_Heat_Exchanger
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Energy-Thermal_Management-Batteries
class Conjugate_Heat_Exchanger(Energy_Component):
    """This provides output values for a direct convention heat exchanger of a bettery pack
    
    Assumptions:
    None
    
    Source:
    N/A
    """
    
    def __defaults__(self):  
        self.tag                                      = 'Atmospheric_Air_Convection_Heat_Exchanger'
        self.cooling_fluid                            = Air()    
        self.cooling_fluid.flowspeed                  = 0.01                                          
        self.convective_heat_transfer_coefficient     = 35.     # [W/m^2K] 
        self.heat_transfer_efficiency                 = 1.0      
        return
    
    def compute_net_generated_battery_heat(self,battery,Q_heat_gen,numerics,freestream): 
  
        return btms_results
        
