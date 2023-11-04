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
def atmospheric_air_HEX_geometry_setup(HEX,HRS): 
    """  
    """     
    vehicle                                        = RCAIDE.Vehicle()  
    net                                            = RCAIDE.Energy.Networks.All_Electric()  
    bus                                            = RCAIDE.Energy.Distributors.Bus_Power_Control_Unit()
    bat                                            = RCAIDE.Energy.Storages.Batteries.Lithium_Ion_NMC()   
    
    HEX                                            = RCAIDE.Energy.Thermal_Management.Batteries.Heat_Exchanger_Systems.Conjugate_Heat_Exchanger()  
    HEX.coolant_flow_rate                          = HRS.coolant_flow_rate
    HEX.coolant_pressure_ratio                     = HRS.coolant_pressure_ratio 
      
    bat.thermal_management_system.heat_exchanger = HEX 
    bus.batteries.append(bat)
    net.busses.append(bus) 
    vehicle.append_energy_network(net)
    
    configs                             = RCAIDE.Components.Configs.Config.Container()
    base_config                         = RCAIDE.Components.Configs.Config(vehicle)  
    config                              = RCAIDE.Components.Configs.Config(base_config)
    config.tag                          = 'optimized'  
    configs.append(config)         
    return configs 