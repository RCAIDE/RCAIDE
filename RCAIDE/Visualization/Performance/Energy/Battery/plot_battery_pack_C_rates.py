## @ingroup Visualization-Performance-Energy-Battery
# RCAIDE/Visualization/Performance/Energy/Battery/plot_battery_C_rating.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  

from RCAIDE.Core import Units
from RCAIDE.Visualization.Performance.Common import set_axes, plot_style,get_battery_names
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np  

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Visualization-Performance-Energy-Battery
def plot_battery_pack_C_rates(results,
                        save_figure   = False,
                        show_legend   = True,
                        save_filename = "Battery_Pack_C_Rates",
                        file_type     =".png",
                        width         = 12,
                        height        = 7):
    """Plots the pack-level conditions of the battery throughout flight.

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
                            pack_energy         = battery_conditions.pack.energy[:,0]
                            pack_volts          = battery_conditions.pack.voltage_under_load[:,0] 
                            pack_current        = battery_conditions.pack.current[:,0] 
                    
                            pack_battery_amp_hr = (pack_energy/ Units.Wh )/pack_volts
                            pack_C_instant      = pack_current/pack_battery_amp_hr
                            pack_C_nominal      = pack_current/np.max(pack_battery_amp_hr) 
                    
                            segment_tag  =  results.segments[i].tag
                            segment_name = segment_tag.replace('_', ' ') 
                             
                            axes_1 = plt.subplot(2,1,1)
                            axes_1.plot(time, pack_C_instant, color = line_colors[i], marker = ps.marker, linewidth = ps.line_width, label = segment_name)
                            axes_1.set_ylabel(r'Inst. C-Rate (C)')
                            axes_1.set_xlabel('Time (mins)')
                            set_axes(axes_1)     
                            
                            axes_2 = plt.subplot(2,1,2)
                            axes_2.plot(time, pack_C_nominal, color = line_colors[i], marker = ps.marker, linewidth = ps.line_width)
                            axes_2.set_ylabel(r'Nom. C-Rate (C)')
                            axes_2.set_xlabel('Time (mins)')
                            set_axes(axes_2)  
        
    
        if show_legend:
            leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 5) 
            leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
        
        # Adjusting the sub-plots for legend 
        fig.subplots_adjust(top=0.8)
        
        # set title of plot 
        title_text    = 'Battery Pack C-Rates: ' + b[b_i]      
        fig.suptitle(title_text)
        
        if save_figure:
            plt.savefig(save_filename + '_' + b[b_i] + file_type)   
    return