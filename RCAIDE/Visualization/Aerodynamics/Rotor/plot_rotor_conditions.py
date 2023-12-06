## @ingroup Visualization-Performance-Aerodynamics-Rotor 
# RCAIDE/Visualization/Performance/Aerodynamics/Rotor/plot_rotor_conditions.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  

from RCAIDE.Core import Units
from RCAIDE.Visualization.Common import set_axes, plot_style 
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

    for network in results.segments[0].analyses.energy.networks: 
        busses  = network.busses
        for bus in busses:     
            for propulsor in bus.propulsors:  
            
                fig = plt.figure(save_filename + '_' + propulsor.tag)
                fig.set_size_inches(width,height)   
                
                for i in range(len(results.segments)): 
                    bus_results  = results.segments[i].conditions.energy[bus.tag] 
                    time         = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min   
                    rpm          =  bus_results[propulsor.tag].rotor.rpm[:,0]
                    thrust       =  bus_results[propulsor.tag].rotor.thrust[:,0]
                    torque       =  bus_results[propulsor.tag].rotor.torque[:,0]
                    tm           =  bus_results[propulsor.tag].rotor.tip_mach[:,0]  
                    segment_tag  =  results.segments[i].tag
                    segment_name = segment_tag.replace('_', ' ')
                    
                    axes_1 = plt.subplot(2,2,1)
                    axes_1.plot(time,rpm, color = line_colors[i], marker = ps.marker  , linewidth = ps.line_width, label = segment_name)
                    axes_1.set_ylabel(r'RPM')
                    set_axes(axes_1)    
                    
                    axes_2 = plt.subplot(2,2,2)
                    axes_2.plot(time, tm, color = line_colors[i], marker = ps.marker  , linewidth = ps.line_width) 
                    axes_2.set_ylabel(r'Tip Mach')
                    set_axes(axes_2) 
            
                    axes_3 = plt.subplot(2,2,3)
                    axes_3.plot(time,thrust, color = line_colors[i], marker = ps.marker , linewidth = ps.line_width)
                    axes_3.set_ylabel(r'Thrust (N)')
                    set_axes(axes_3) 
                    
                    axes_4 = plt.subplot(2,2,4)
                    axes_4.plot(time,torque, color = line_colors[i], marker = ps.marker , linewidth = ps.line_width)
                    axes_4.set_ylabel(r'Torque (N-m)')
                    set_axes(axes_4)     
                    
                if show_legend:            
                    leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 5) 
                    leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
                
                # Adjusting the sub-plots for legend 
                fig.subplots_adjust(top=0.8) 
                
                # set title of plot 
                title_text  =  'Rotor Performance: ' + propulsor.tag
                fig.suptitle(title_text)
                if save_figure:
                    plt.savefig(save_filename + '_' + propulsor.tag + file_type)   
    return fig 