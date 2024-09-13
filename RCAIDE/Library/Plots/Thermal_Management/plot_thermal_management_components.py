# @ingroup Visualization-Performance-Energy-Thermal_Management
# RCAIDE/Visualization/Performance/Energy/Thermal_Management/plot_heat_acquisition_system_conditions.py
# 
# 
# Created:  Sep 2024, S. Shekar


# ----------------------------------------------------------------------------------------------------------------------
#   plot_thermal_management_component
# ----------------------------------------------------------------------------------------------------------------------   

def plot_thermal_management_component(results,
                        save_figure   = False,
                        show_legend   = True,
                        save_filename = 'Thermal Management Component', 
                        file_type     =".png",
                        width         = 12,
                        height        = 7):
    
    for network in  results.segments[0].analyses.energy.vehicle.networks:
        for coolant_line in  network.coolant_lines:
            for tag, item in  coolant_line.items(): 
                if tag == 'batteries':
                    for battery in item:
                        for btms in  battery:
                            btms.plot_operating_conditions(results,coolant_line,save_figure,show_legend,btms.tag,file_type,width, height)
                if tag == 'heat_exchangers':
                    for heat_exchanger in  item:
                        heat_exchanger.plot_operating_conditions(results,coolant_line,save_figure,show_legend,heat_exchanger.tag,file_type,width, height)
                if tag == 'reservoirs':
                    for reservoir in  item:
                        reservoir.plot_operating_conditions(results,coolant_line,save_figure,show_legend,reservoir.tag,file_type,width, height)             
            
        
    return