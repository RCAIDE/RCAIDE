# @ingroup Visualization-Performance-Energy-Thermal_Management
# RCAIDE/Visualization/Performance/Energy/Thermal_Management/plot_heat_acquisition_system_conditions.py
# 
# 
# Created:  Jul 2023, M. Clarke


# ----------------------------------------------------------------------------------------------------------------------
#   plot_heat_exchanger_system_conditions
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Visualization-Performance-Energy-Thermal_Management
def plot_thermal_management_component(results):
    
    for network in  results.segments[0].analyses.energy.vehicle.networks:
        for coolant_line in  network.coolant_lines:
            for tag, item in  coolant_line.items(): 
                if tag == 'batteries':
                    for battery in item:
                        for btms in  battery:
                            btms.plot_operating_conditions(results, coolant_line)
                if tag == 'heat_exchangers':
                    for heat_exchanger in  item:
                        heat_exchanger.plot_operating_conditions(results, coolant_line)
                if tag == 'reservoirs':
                    for reservoir in  item:
                        reservoir.plot_operating_conditions(results, coolant_line)             
            
        
    return