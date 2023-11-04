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

## @ingroup Methods-Thermal_Management-Batteries-Sizing
def wavy_channel_geometry_setup(HRS,battery): 
    """  
    """     
    vehicle                             = RCAIDE.Vehicle()  
    net                                 = RCAIDE.Energy.Networks.All_Electric()  
    bus                                 = RCAIDE.Energy.Distributors.Bus_Power_Control_Unit()     
    battery.thermal_management_system.heat_removal_system = HRS 
    bus.batteries.append(battery)
    net.busses.append(bus) 
    vehicle.append_energy_network(net) 
    configs                             = RCAIDE.Components.Configs.Config.Container()
    base_config                         = RCAIDE.Components.Configs.Config(vehicle)  
    config                              = RCAIDE.Components.Configs.Config(base_config)
    config.tag                          = 'optimized'  
    configs.append(config)         
    return configs 