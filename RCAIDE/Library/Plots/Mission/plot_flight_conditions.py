## @defgroup Library-Plots-Mission  
# RCAIDE/Library/Plots/Performance/Mission/plot_flight_conditions.py
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
## @defgroup Library-Plots-Mission  
def plot_flight_conditions(results,
                           save_figure = False,
                           show_legend=True,
                           save_filename = "Flight Conditions",
                           file_type = ".png",
                           width = 12, height = 7): 

    """This plots the flights the conditions

    Assumptions:
    None

    Source:
    None

    Inputs:
    results.segments.conditions.
         frames
             body.inertial_rotations
             inertial.position_vector
         freestream.velocity
         aerodynamics.
             lift_coefficient
             drag_coefficient
             angle_of_attack

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
     
    fig   = plt.figure(save_filename)
    fig.set_size_inches(width,height) 
    for i in range(len(results.segments)): 
        time     = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        airspeed = results.segments[i].conditions.freestream.velocity[:,0] /   Units['mph']
        theta    = results.segments[i].conditions.frames.body.inertial_rotations[:,1,None] / Units.deg
        Range    = results.segments[i].conditions.frames.inertial.aircraft_range[:,0]/ Units.nmi
        altitude = results.segments[i].conditions.freestream.altitude[:,0]/Units.feet
              
        segment_tag  =  results.segments[i].tag
        segment_name = segment_tag.replace('_', ' ')
        
        axis_1 = plt.subplot(2,2,1)
        axis_1.plot(time, altitude, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = segment_name)
        axis_1.set_ylabel(r'Altitude (ft)')
        set_axes(axis_1)    
        
        axis_2 = plt.subplot(2,2,2)
        axis_2.plot(time, airspeed, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width) 
        axis_2.set_ylabel(r'Airspeed (mph)')
        set_axes(axis_2) 
        
        axis_3 = plt.subplot(2,2,3)
        axis_3.plot(time, Range, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width)
        axis_3.set_xlabel('Time (mins)')
        axis_3.set_ylabel(r'Range (nmi)')
        set_axes(axis_3) 
         
        axis_4 = plt.subplot(2,2,4)
        axis_4.plot(time, theta, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width)
        axis_4.set_xlabel('Time (mins)')
        axis_4.set_ylabel(r'Pitch Angle (deg)')
        set_axes(axis_4) 
         
    
    if show_legend:        
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 5) 
        leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
    
    # Adjusting the sub-plots for legend 
    fig.subplots_adjust(top=0.8)
    
    # set title of plot 
    title_text    = 'Flight Conditions'      
    fig.suptitle(title_text)
    
    if save_figure:
        plt.savefig(save_filename + file_type)   
    return  fig 