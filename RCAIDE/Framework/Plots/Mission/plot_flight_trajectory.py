# RCAIDE/Library/Plots/Performance/Functions/plot_flight_trajectory.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
from RCAIDE.Framework.Core import Units
from RCAIDE.Framework.Plots.Common import set_axes, plot_style
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np  

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------             
def plot_flight_trajectory(results,
                           line_color = 'bo-',
                           line_color2 = 'rs--',
                           save_figure = False,
                           show_legend   = True,
                           save_filename = "Flight_Trajectory",
                           file_type = ".png",
                           width = 12, height = 7):
    """This plots the 3D flight trajectory of the aircraft.

    Assumptions:
        None

    Source:
        None

    Args:
        results (dict): results data structure

    Returns:
        fig     (figure) 
	
    """	     

    # get plotting style 
    ps      = plot_style()  

    parameters = {'axes.labelsize': ps.axis_font_size,
                  'xtick.labelsize': ps.axis_font_size,
                  'ytick.labelsize': ps.axis_font_size,
                  'axes.titlesize': ps.title_font_size}
    plt.rcParams.update(parameters) 
        
    fig = plt.figure(save_filename)
    fig.set_size_inches(width,height) 
     
    # get line colors for plots 
    line_colors   = cm.inferno(np.linspace(0,0.9,len(results.segments)))    
     
    for i, segment in enumerate(results.segments):
        time     = segment.conditions.frames.inertial.time[:,0] / Units.min
        Range    = segment.conditions.frames.inertial.aircraft_range[:,0]/Units.nmi
        x        = segment.conditions.frames.inertial.position_vector[:,0]  
        y        = segment.conditions.frames.inertial.position_vector[:,1] 
        z        = -segment.conditions.frames.inertial.position_vector[:,2] 

        segment_tag  =  segment.tag
        segment_name = segment_tag.replace('_', ' ')
        
        axes = plt.subplot(2,2,1)
        axes.plot( time , Range, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width , label = segment_name)
        axes.set_ylabel('Distance (nmi)')
        axes.set_xlabel('Time (min)')
        set_axes(axes)            

        axes = plt.subplot(2,2,2)
        axes.plot(x, y , line_color, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width )
        axes.set_xlabel('x (m)')
        axes.set_ylabel('y (m)')
        set_axes(axes)

        axes = plt.subplot(2,2,3)
        axes.plot( time , z, line_color , color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width )
        axes.set_ylabel('z (m)')
        axes.set_xlabel('Time (min)')
        set_axes(axes)   
        
        axes = plt.subplot(2,2,4, projection='3d') 
        axes.scatter(x, y, z, marker='o',color =  line_colors[i])
        axes.set_xlabel('x')
        axes.set_ylabel('y')
        axes.set_zlabel('z') 
        set_axes(axes)         
        
    if show_legend:        
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 5) 
        leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
    
    # Adjusting the sub-plots for legend 
    fig.subplots_adjust(top=0.8)
    
    # set title of plot 
    title_text    = 'Flight Trajectory'      
    fig.suptitle(title_text)
    
    if save_figure:
        plt.savefig(save_filename + file_type)   
             
    return fig         