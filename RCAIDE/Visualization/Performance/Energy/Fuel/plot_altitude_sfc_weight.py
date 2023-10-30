## @ingroup Visualization-Geometry-Three_Dimensional
# RCAIDE/Visualization/Performance/Energy/Fuel/plot_altitude_sfc_weight.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
from RCAIDE.Core import Units
from RCAIDE.Visualization.Performance.Common import set_axes, plot_style, get_propulsor_group_names
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Visualization-Performance-Energy-Fuel
def plot_altitude_sfc_weight(results,
                             save_figure = False,
                             show_legend = True,
                             save_filename = "Altitude_SFC_Weight" ,
                             file_type = ".png",
                             width = 12, height = 7):
    """This plots the altitude, specific fuel consumption and vehicle weight.

    Assumptions:
    None

    Source:

    Depricated RCAIDE Mission Plots Functions

    Created:    Mar 2020, M. Clarke
    Modified:   Apr 2020, M. Clarke
                Sep 2020, M. Clarke
                Apr 2021, M. Clarke
                Dec 2021, S. Claridge


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
    pg = get_propulsor_group_names(results)    
     
    fig   = plt.figure(save_filename)
    fig.set_size_inches(width,height)
    
    for i in range(len(results.segments)): 
        time     = results.segments[i].conditions.frames.inertial.time[:, 0] / Units.min
        Weight   = results.segments[i].conditions.weights.total_mass[:, 0] * 9.81   
        mdot     = results.segments[i].conditions.weights.vehicle_mass_rate[:, 0]
        thrust   = results.segments[i].conditions.frames.body.thrust_force_vector[:, 0]
        sfc      = (mdot / Units.lb) / (thrust / Units.lbf) * Units.hr       
            
        segment_tag  =  results.segments[i].tag
        segment_name = segment_tag.replace('_', ' ') 
        
        # power 
        axes_1 = plt.subplot(2,2,1)
        axes_1.set_ylabel(r'Throttle')
        set_axes(axes_1)               
        for pg_i in range(len(pg)): 
            for network in results.segments[i].analyses.energy.networks: 
                busses      = network.busses
                fuel_lines  = network.fuel_lines
                for bus in busses:  
                    plot_propulsor_throttles(results,bus,i,pg,pg_i,time,line_colors,ps,segment_name,axes_1)           
                for fuel_line in fuel_lines: 
                    plot_propulsor_throttles(results,fuel_line,i,pg,pg_i,time,line_colors,ps,segment_name,axes_1) 
                    
        
        axes_2 = plt.subplot(2,2,2)
        axes_2.plot(time, Weight/1000 , color = line_colors[i], marker = ps.marker, linewidth = ps.line_width) 
        axes_2.set_ylabel(r'Weight (kN)')  
        set_axes(axes_2) 

        axes_3 = plt.subplot(2,2,3)
        axes_3.plot(time, sfc, color = line_colors[i], marker = ps.marker, linewidth = ps.line_width)
        axes_3.set_xlabel('Time (mins)')
        axes_3.set_ylabel(r'SFC (lb/lbf-hr)')
        set_axes(axes_3) 

        axes_3 = plt.subplot(2,2,4)
        axes_3.plot(time, mdot, color = line_colors[i], marker = ps.marker, linewidth = ps.line_width)
        axes_3.set_xlabel('Time (mins)')
        axes_3.set_ylabel(r'Fuel Rate (kg/s)')
        set_axes(axes_3)         
        
    
    if show_legend:
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 5) 
        leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
    
    # Adjusting the sub-plots for legend 
    fig.subplots_adjust(top=0.8)
    
    # set title of plot 
    title_text    = 'Throttle SFC and Weight'      
    fig.suptitle(title_text)
    
    if save_figure:
        plt.savefig(save_filename + file_type)   
    return


def plot_propulsor_throttles(results,distributor,i,pg,pg_i,time,line_colors,ps,segment_name,axes_1): 
    active_propulsor_groups   = distributor.active_propulsor_groups    
    results               = results.segments[i].conditions.energy[distributor.tag] 
    for j in range(len(active_propulsor_groups)):  
        if pg[pg_i] == active_propulsor_groups[j]:  
            if 'engine' in  results[active_propulsor_groups[j]]:  
                eta    =   results[active_propulsor_groups[j]].engine.throttle[:,0]
            elif 'motor' in  results[active_propulsor_groups[j]]:
                eta    =   results[active_propulsor_groups[j]].motor.throttle[:,0]   
            elif 'turbofan' in  results[active_propulsor_groups[j]]:
                eta    =   results[active_propulsor_groups[j]].turbofan.throttle[:,0]  
            elif 'turbojet' in  results[active_propulsor_groups[j]]:
                eta    =  results[active_propulsor_groups[j]].turbojet.throttle[:,0]  

            axes_1.plot(time, eta, color = line_colors[i], marker = ps.marker, linewidth = ps.line_width, label = segment_name)         
    return       