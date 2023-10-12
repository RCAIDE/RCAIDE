## @ingroup Methods-Thermal_Management-Batteries-Sizing
# btms_geometry_setup.py 
#
# Created: Jun 2023, M. Clarke

# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------  
# RCAIDE Imports 
import RCAIDE    
from RCAIDE.Components.Energy.Thermal_Management.Batteries.Channel_Cooling.Wavy_Channel_Gas_Liquid_Heat_Exchanger                       import Wavy_Channel_Gas_Liquid_Heat_Exchanger 
from RCAIDE.Components.Energy.Thermal_Management.Batteries.Atmospheric_Air_Convection_Cooling.Atmospheric_Air_Convection_Heat_Exchanger import Atmospheric_Air_Convection_Heat_Exchanger 

# Python package imports   
import numpy as np  

## @ingroup Methods-Thermal_Management-Batteries-Sizing
def btms_geometry_setup(bat_0): 
    """  
    """     
    vehicle                                        = RCAIDE.Vehicle()  
    net                                            = RCAIDE.Components.Energy.Networks.Battery_Electric_Rotor() 
    # Component 5: the Battery
    bat                                            = RCAIDE.Components.Energy.Storages.Batteries.Constant_Mass.Lithium_Ion_LiNiMnCoO2_18650() 
    bat.pack_config.series                         = bat_0.pack_config.series                        
    bat.pack_config.parallel                       = bat_0.pack_config.parallel                     
    bat.pack_config.total                          = bat_0.pack_config.total                        
    initialize_from_circuit_configuration(bat_0)         
    net.voltage                                    = net.voltage                                  
    bat.module_config.number_of_modules            = bat_0.module_config.number_of_modules          
    bat.module_config.normal_count                 = bat_0.module_config.normal_count               
    bat.module_config.parallel_count               = bat_0.module_config.parallel_count             
    bat.module_config.total                        = bat_0.module_config.total                      
    bat.module_config.voltage                      = bat_0.module_config.voltage                    
    bat.air_cooled                                 = bat_0.air_cooled         

    if type(bat_0.thermal_management_system) == Wavy_Channel_Gas_Liquid_Heat_Exchanger:
        btms                                                = RCAIDE.Components.Energy.Thermal_Management.Batteries.Channel_Cooling.Wavy_Channel_Gas_Liquid_Heat_Exchanger() 
        btms.hex.length_of_hot_fluid                        = 0.6    # L_h
        btms.hex.length_of_cold_fluid                       = 0.9    # L_c
        btms.hex.stack_height                               = 0.24   # H
        btms.hex.hydraulic_diameter_of_hot_fluid_channel    = 5e-4   # d_H_h
        btms.hex.aspect_ratio_of_hot_fluid_channel          = 1      # gamma_h 
        btms.hex.hydraulic_diameter_of_cold_fluid_channel   = 1e-2   # d_H_c
        btms.hex.aspect_ratio_of_cold_fluid_channel         = 3      # gamma_c  
        btms.hex.mass_flow_rate_of_hot_fluid                = 1  # m_dot_h
        btms.hex.mass_flow_rate_of_cold_fluid               = 2      # m_dot_c
        btms.hex.pressure_ratio_of_hot_fluid                = 0.7    # PI_c
        btms.hex.pressure_ratio_of_cold_fluid               = 0.98   # PI_h
        btms.hex.pressure_at_inlet_of_hot_fluid             = 101325 # p0_h
        btms.wavychan.number_of_channels_per_module         = 15  
    
    if 
    net.btms                                            = btms 

    
    
    net.battery.append(battery)  
    vehicle.append_component(net)
    
    configs                             = RCAIDE.Components.Configs.Config.Container()
    base_config                         = RCAIDE.Components.Configs.Config(vehicle) 
    
    config                              = RCAIDE.Components.Configs.Config(base_config)
    config.tag                          = 'optimized'  
    configs.append(config)         
    return configs 