## @ingroup Visualization-Performance-Energy-Thermal_Management
# RCAIDE/Visualization/Performance/Energy/Thermal_Management/plot_heat_acquisition_system_conditions.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  

from RCAIDE.Framework.Core import Units
from RCAIDE.Library.Plots.Common import set_axes, plot_style
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#   plot_heat_exchanger_system_conditions
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Visualization-Performance-Energy-Thermal_Management
def plot_air_cooled_conditions(air_cooled, results, coolant_line, save_figure,show_legend ,save_filename,file_type , width, height):
    """Plots the cell-level conditions of the battery throughout flight.

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.conditions.
       ADD SAI

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

    fig = plt.figure(save_filename)
    fig.set_size_inches(width,height) 
    axis_0 = plt.subplot(1,1,1)
    axis_1 = plt.subplot(2,1,1)
    axis_2 = plt.subplot(2,1,2)        
    b_i = 0 
   
    axis_0.plot(np.zeros(2),np.nan*np.zeros(2), color = line_colors[0], marker = ps.markers[b_i], linewidth = ps.line_width, label = wavy_channel.tag) 
    axis_0.grid(False)
    axis_0.axis('off')  
   
    for i in range(len(results.segments)):  
        time                       = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min    
        air_cooled_conditions      = results.segments[i].conditions.energy[coolant_line.tag][air_cooled.tag]   
        effectiveness              = air_cooled_conditions.effectiveness[:,0]
        total_heat_removed         = air_cooled_conditions.coolant_mass_flow_rate[:,0]
        segment_tag                = results.segments[i].tag
        segment_name               = segment_tag.replace('_', ' ') 

        if b_i == 0:                     
            axis_1.plot(time, effectiveness, color = line_colors[i], marker = ps.markers[b_i], linewidth = ps.line_width, label = segment_name)
        else:
            axis_1.plot(time, effectiveness, color = line_colors[i], marker = ps.markers[b_i], linewidth = ps.line_width)
        axis_1.set_ylabel(r'Effectiveness') 
        set_axes(axis_1)     
         
        axis_2.plot(time, total_heat_removed, color = line_colors[i], marker = ps.markers[b_i], linewidth = ps.line_width)
        axis_2.set_ylabel(r'Total Heat Removed (W)')
        set_axes(axis_2) 
              
        b_i += 1 
            
    if show_legend:      
        h, l = axis_1.get_legend_handles_labels()
        axis_1.legend(h, l)    
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 5) 
        leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})     
    
    # Adjusting the sub-plots for legend 
    fig.subplots_adjust(top=0.8) 
    
    # set title of plot 
    title_text   = 'Air_Cooled_Properties'       
    fig.suptitle(title_text) 
    
    if save_figure:
        plt.savefig(save_filename + air_cooled.tag + file_type)    
    return fig     