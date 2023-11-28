## @ingroup Methods-Thermal_Management-Batteries-Sizing
# btms_geometry_setup.py 
#
# Created: Jun 2023, M. Clarke

# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------  
# RCAIDE Imports 
import RCAIDE     

# Python package imports   

import numpy as np  

## @ingroup Methods-Thermal_Management-Batteries-Sizing
def cross_flow_heat_exchanger_geometry_setup(HEX,HAS): 
    """  
    """     
    vehicle                                        = RCAIDE.Vehicle()  
    net                                            = RCAIDE.Energy.Networks.All_Electric()  
    bus                                            = RCAIDE.Energy.Distributors.Bus_Power_Control_Unit()
    bat                                            = RCAIDE.Energy.Storages.Batteries.Lithium_Ion_NMC()   
     
    HEX.coolant_flow_rate                          = HAS.coolant_flow_rate #1.0
   # HEX.coolant_pressure_drop                      = HAS.coolant_pressure_drop
    HEX.coolant_temperature_of_hot_fluid           = 303 #HAS.coolant_outlet_temperature #50
    bat.thermal_management_system.heat_exchanger   = HEX 
    bus.batteries.append(bat)
    net.busses.append(bus) 
    vehicle.append_energy_network(net)
    
    configs                             = RCAIDE.Components.Configs.Config.Container()
    base_config                         = RCAIDE.Components.Configs.Config(vehicle)  
    config                              = RCAIDE.Components.Configs.Config(base_config)
    config.tag                          = 'optimized'  
    configs.append(config)         
    return configs 