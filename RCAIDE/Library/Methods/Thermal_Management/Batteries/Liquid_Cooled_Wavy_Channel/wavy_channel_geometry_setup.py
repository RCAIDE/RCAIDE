
#RCAIDE/Library/Methods/Thermal_Management/Batteries/Liquid_Cooled_Wavy_Channel/wavy_channel_geometry_setup.py
#
# Created: Apr 2024, S. Shekar 2024

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE     

# ----------------------------------------------------------------------------------------------------------------------  
#  Wavy Channel Geometry Setup 
# ----------------------------------------------------------------------------------------------------------------------   

def wavy_channel_geometry_setup(HAS,battery): 
    """ Defines a dummy vehicle for wavy channel geometry optimization.
          
          Inputs:  
             HAS   - HAS data structure             [None] 
             battery - Battery data structure
         Outputs:  
             configs - configuration used in optimization    [None]
              
          Assumptions: 
             N/A 
        
          Source:
             None
    """     
    vehicle                                                   = RCAIDE.Vehicle()  
    net                                                       = RCAIDE.Framework.Networks.Electric()  
    bus                                                       = RCAIDE.Library.Components.Energy.Distributors.Electrical_Bus()     
    battery.thermal_management_system.heat_acquisition_system = HAS 
    bus.batteries.append(battery)
    net.busses.append(bus) 
    vehicle.append_energy_network(net) 
    configs                                                     = RCAIDE.Library.Components.Configs.Config.Container()
    base_config                                                 = RCAIDE.Library.Components.Configs.Config(vehicle)  
    config                                                      = RCAIDE.Library.Components.Configs.Config(base_config)
    config.tag                                                  = 'optimized'  
    configs.append(config)         
    return configs 