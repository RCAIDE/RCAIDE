## @ingroup Visualization-Performance-Aerodynamics-Rotor 
# RCAIDE/Visualization/Performance/Aerodynamics/Rotor/plot_rotor_conditions.py
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
## @ingroup Visualization-Performance-Aerodynamics-Rotor 
def plot_rotor_conditions(results,
                        save_figure = False,
                        show_legend=True,
                        save_filename = "Rotor_Conditions",
                        file_type = ".png",
                        width = 12, height = 7):
    """This plots the electric driven network propeller efficiencies 

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.conditions.propulsion.  
        
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
    
    for pg_i in range(len(pg)): 
        fig = plt.figure(save_filename + '_' + pg[pg_i])
        fig.set_size_inches(width,height) 
            
        for i in range(len(results.segments)): 
            time    = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min 
            for network in results.segments[i].analyses.energy.networks: 
                busses  = network.busses
                for bus in busses: 
                    active_propulsor_groups   = bus.active_propulsor_groups    
                    bus_results               = results.segments[i].conditions.energy[bus.tag] 
                    for j in range(len(active_propulsor_groups)):  
                        if pg[pg_i] == active_propulsor_groups[j]: 
                            rpm    =  bus_results[active_propulsor_groups[j]].rotor.rpm[:,0]
                            thrust =  np.linalg.norm(results.segments[i].conditions.frames.body.thrust_force_vector[:,:],axis=1)
                            torque =  bus_results[active_propulsor_groups[j]].motor.torque[:,0]
                            tm     =  bus_results[active_propulsor_groups[j]].rotor.tip_mach[:,0]
                            Cp     =  bus_results[active_propulsor_groups[j]].rotor.power_coefficient[:,0]
                            eta    =  bus_results[active_propulsor_groups[j]].motor.throttle[:,0]
                             
                            segment_tag  =  results.segments[i].tag
                            segment_name = segment_tag.replace('_', ' ')
                            
                            axes_1 = plt.subplot(3,2,1)
                            axes_1.plot(time,rpm, color = line_colors[i], marker = ps.marker  , linewidth = ps.line_width, label = segment_name)
                            axes_1.set_ylabel(r'RPM')
                            set_axes(axes_1)    
                            
                            axes_2 = plt.subplot(3,2,2)
                            axes_2.plot(time, tm, color = line_colors[i], marker = ps.marker  , linewidth = ps.line_width) 
                            axes_2.set_ylabel(r'Tip Mach')
                            set_axes(axes_2) 
                    
                            axes_3 = plt.subplot(3,2,3)
                            axes_3.plot(time,thrust, color = line_colors[i], marker = ps.marker , linewidth = ps.line_width)
                            axes_3.set_ylabel(r'Thrust (N)')
                            set_axes(axes_3) 
                            
                            axes_4 = plt.subplot(3,2,4)
                            axes_4.plot(time,torque, color = line_colors[i], marker = ps.marker , linewidth = ps.line_width)
                            axes_4.set_ylabel(r'Torque (N-m)')
                            set_axes(axes_4)    
                            
                            axes_5 = plt.subplot(3,2,5)
                            axes_5.plot(time, Cp, color = line_colors[i], marker = ps.marker  , linewidth = ps.line_width)
                            axes_5.set_xlabel('Time (mins)')
                            axes_5.set_ylabel(r'Power Coefficient')
                            set_axes(axes_5) 
                    
                            axes_6 = plt.subplot(3,2,6)
                            axes_6.plot(time, eta, color = line_colors[i], marker = ps.marker  , linewidth = ps.line_width)
                            axes_6.set_xlabel('Time (mins)')
                            axes_6.set_ylabel(r'Throttle')
                            set_axes(axes_6) 
                            
                    
        if show_legend:            
            leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 5) 
            leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
        
        # Adjusting the sub-plots for legend 
        fig.subplots_adjust(top=0.8)
        
        # set title of plot 
        title_text  =  'Rotor Conditions: ' + pg[pg_i]     
        fig.suptitle(title_text)
        
        if save_figure:
            plt.savefig(save_filename + '_' + pg[pg_i] + file_type)   
    return