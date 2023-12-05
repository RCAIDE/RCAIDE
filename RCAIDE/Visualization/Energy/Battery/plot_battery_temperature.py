## @ingroup Visualization-Geometry-Three_Dimensional
# RCAIDE/Visualization/Performance/Energy/Battery/plot_battery_health_conditions.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  

from RCAIDE.Core import Units
from RCAIDE.Visualization.Common import set_axes, plot_style , get_battery_names
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Visualization-Performance-Energy-Battery
def plot_battery_temperature(results,
                                  save_figure = False,
                                  show_legend = True,
                                  save_filename = "Battery_Temperature",
                                  file_type = ".png",
                                  width = 12, height = 7):
    """Plots the cell-level conditions of the battery throughout flight.

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.conditions.
        freestream.altitude
        weights.total_mass
        weights.vehicle_mass_rate
        frames.body.thrust_force_vector

    Outputs: 
    Plots

    Properties Used:
    N/A	
    """ 
    
    # get plotting style 
    ps      = plot_style()  

    parameters = {'axes.labelsize': ps.axis_font_size,
                  'xtick.labelsize': ps.axis_font_size,
                  'ytick.labelsize': ps.axis_font_size,
                  'axes.titlesize': ps.title_font_size}
    plt.rcParams.update(parameters)
     
    # get line colors for plots 
    line_colors   = cm.inferno(np.linspace(0,0.9,len(results.segments)))     
    
    # compile a list of all propulsor group names on aircraft 
    b = get_battery_names(results)
    
    for b_i in range(len(b)): 
        fig = plt.figure(save_filename + '_' + b[b_i])
        fig.set_size_inches(width,height) 
             
        for i in range(len(results.segments)): 
            time    = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min 
            for network in results.segments[i].analyses.energy.networks: 
                busses  = network.busses
                for bus in busses: 
                    for battery in bus.batteries:
                        if battery.tag == b[b_i]:  
                            battery_conditions  = results.segments[i].conditions.energy[bus.tag][battery.tag]  
                            cell_temp           = battery_conditions.cell.temperature[:,0]
                            cell_charge         = battery_conditions.cell.charge_throughput[:,0]
                            pack_Q              = battery_conditions.pack.heat_energy_generated[:,0]
                    
                            segment_tag  =  results.segments[i].tag
                            segment_name = segment_tag.replace('_', ' ')  
                    
                            axes_1 = plt.subplot(2,2,1)
                            axes_1.plot(time,cell_temp, color = line_colors[i], marker = ps.marker, linewidth = ps.line_width)
                            axes_1.set_ylabel(r'Temperature (K)') 
                            set_axes(axes_1)        
                            
                            axes_2 = plt.subplot(2,2,2)
                            axes_2.plot(time, cell_charge, color = line_colors[i], marker = ps.marker, linewidth = ps.line_width, label = segment_name)
                            axes_2.set_xlabel('Time (mins)')
                            axes_2.set_ylabel(r'Charge Throughput (Ah)')
                            set_axes(axes_2)  
 
                            
                            axes_3 = plt.subplot(2,2,3)
                            axes_3.plot(time, pack_Q/1000, color = line_colors[i], marker = ps.marker, linewidth = ps.line_width, label = segment_name)
                            axes_3.set_xlabel('Time (mins)')
                            axes_3.set_ylabel(r'$\dot{Q}_{heat}$ (kW)')
                            set_axes(axes_3)                              
                    
    
        if show_legend:        
            leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 5) 
            leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
        
        # Adjusting the sub-plots for legend 
        fig.subplots_adjust(top=0.8)
        
        # set title of plot 
        title_text    = 'Battery Health: ' + b[b_i]      
        fig.suptitle(title_text)
        
        if save_figure:
            plt.savefig(save_filename + '_' + b[b_i] + file_type)   
    return fig 