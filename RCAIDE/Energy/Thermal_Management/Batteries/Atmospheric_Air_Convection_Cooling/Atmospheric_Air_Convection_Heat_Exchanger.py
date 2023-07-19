## @ingroup Components-Energy-Thermal_Management
# Atmospheric_Air_Convection_Heat_Exchanger.py
#
# Created: Jun 2023. M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ---------------------------------------------------------------------- 
import numpy as np
from MARC.Core import Data
from MARC.Components.Energy.Energy_Component import Energy_Component 
from MARC.Methods.Thermal_Management.Batteries.Direct_Convection_Cooling.direct_convection_model import compute_net_convected_heat 
from MARC.Attributes.Gases import Air

# ----------------------------------------------------------------------
#  Cryogenic Heat Exchanger Component
# ----------------------------------------------------------------------
## @ingroup Components-Energy-Thermal_Management

class Atmospheric_Air_Convection_Heat_Exchanger(Energy_Component):
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
    
    def compute_net_generated_battery_heat(self,battery,Q_heat_gen,numerics): 
        '''
        '''
        Q_heat_gen_tot,  P_net,  T_ambient, T_current =  compute_net_convected_heat(self,battery,Q_heat_gen,numerics) 

        btms_results = Data()
        btms_results.operating_conditions = Data(battery_current_temperature = T_current,
                                                 heat_energy_generated       = Q_heat_gen_tot )   
        return btms_results
        
