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
def atmospheric_air_HEX_geometry_setup(): 
    """  
    """     
    vehicle                                        = RCAIDE.Vehicle()  
    net                                            = RCAIDE.Energy.Networks.All_Electric()  
    bus                                            = RCAIDE.Energy.Distributors.Bus_Power_Control_Unit()
    bat                                            = RCAIDE.Energy.Storages.Batteries.Lithium_Ion_NMC()   
    
    HEX                                            = RCAIDE.Energy.Thermal_Management.Batteries.Heat_Exchanger_Systems.Conjugate_Heat_Exchanger()
    HEX.length_of_hot_fluid                        = 0.6    # L_h
    HEX.length_of_cold_fluid                       = 0.9    # L_c
    HEX.stack_height                               = 0.24   # H
    HEX.hydraulic_diameter_of_hot_fluid_channel    = 5e-4   # d_H_h
    HEX.aspect_ratio_of_hot_fluid_channel          = 1      # gamma_h 
    HEX.air_hydraulic_diameter   = 1e-2   # d_H_c
    HEX.aspect_ratio_of_cold_fluid_channel         = 3      # gamma_c  
    HEX.mass_flow_rate_of_hot_fluid                = 1  # m_dot_h
    HEX.air_flow_rate               = 2      # m_dot_c
    HEX.coolant_pressure_ratio                = 0.7    # PI_c
    HEX.air_pressure_ratio               = 0.98   # PI_h
    HEX.coolant_inlet_pressure             = 101325 # p0_h 
      
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