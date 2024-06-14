## @ingroup Library-Plots-Stability
# RCAIDE/Library/Plots/Stability/plot_stability_forces_and_moments.py
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
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Library-Plots-Stability
def plot_flight_forces_and_moments(results,
                             save_figure = False,
                             show_legend = True,
                             save_filename = "Intertial_Forces_and_Moments",
                             file_type = ".png",
                             width = 12, height = 8):
    """This plots the aerodynamic forces 
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
  
    
    fig   = plt.figure(save_filename)
    fig.set_size_inches(width,height) 

    axis_1 = plt.subplot(3,2,1)
    axis_2 = plt.subplot(3,2,2)
    axis_3 = plt.subplot(3,2,3)
    axis_4 = plt.subplot(3,2,4)
    axis_5 = plt.subplot(3,2,5)  
    axis_6 = plt.subplot(3,2,6)    
    
    for i in range(len(results.segments)): 
        time   = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min 
        X = results.segments[i].conditions.frames.inertial.total_force_vector[:,0]
        Y = results.segments[i].conditions.frames.inertial.total_force_vector[:,1]
        Z = results.segments[i].conditions.frames.inertial.total_force_vector[:,2]
        L = results.segments[i].conditions.frames.inertial.total_moment_vector[:,0]
        M = results.segments[i].conditions.frames.inertial.total_moment_vector[:,1]
        N = results.segments[i].conditions.frames.inertial.total_moment_vector[:,2]
        
                       
        segment_tag  =  results.segments[i].tag
        segment_name = segment_tag.replace('_', ' ') 
        axis_1.plot(time,X, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name) 
        axis_1.set_ylabel(r'X Moment (N)')
        axis_1.set_ylim([-1000, 1000]) 
        set_axes(axis_1)                
        
        axis_2.set_ylabel(r'Roll Moment (Nm)')
        axis_2.plot(time,L, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width) 
        axis_2.set_ylim([-1000, 1000]) 
        set_axes(axis_2)     
        
        axis_3.plot(time,Y, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width) 
        axis_3.set_ylabel(r'Y force (N)')
        axis_3.set_ylim([-1000, 1000]) 
        set_axes(axis_3)  
        
        axis_4.plot(time,M, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width) 
        axis_4.set_ylabel(r'Pitch Moment (Nm)')
        axis_4.set_ylim([-1000, 1000]) 
        set_axes(axis_4) 

        axis_5.plot(time, Z, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width)
        axis_5.set_xlabel('Time (mins)')
        axis_5.set_ylabel(r'Z Force (m)')
        axis_5.set_ylim([-1000, 1000]) 
        set_axes(axis_5)    

        axis_6.plot(time, N, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width)
        axis_6.set_xlabel('Time (mins)')
        axis_6.set_ylabel(r'Yaw Moment (Nm)')
        axis_6.set_ylim([-1000, 1000]) 
        set_axes(axis_6)   
 
    if show_legend:    
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 5) 
        leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
    
    # Adjusting the sub-plots for legend 
    fig.tight_layout()
    fig.subplots_adjust(top=0.8) 
    
    # set title of plot 
    title_text    = 'Intertial Forces and Moments'      
    fig.suptitle(title_text)
    
    if save_figure:
        plt.savefig(save_filename + file_type)   
    return fig 
