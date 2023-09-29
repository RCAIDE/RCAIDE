## @ingroup Visualization-Performance-Aerodynamics-Vehicle
# RCAIDE/Visualization/Performance/Aerodynamics/Vehicle/plot_aerodynamic_forces.py
# (c) Copyright 2023 Aerospace Research Community LLC
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
## @ingroup Visualization-Performance-Aerodynamics-Vehicle
def plot_aerodynamic_forces(results,
                             save_figure = False,
                             show_legend = True,
                             save_filename = "Aerodynamic_Forces",
                             file_type = ".png",
                             width = 12, height = 7):
    """This plots the aerodynamic forces
    
    Assumptions:
    None
    
    Source:
    None
    
    Inputs:
    results.segments.condtions.frames
         body.thrust_force_vector
         wind.lift_force_vector
         wind.drag_force_vector
         
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
        time   = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min
        Power  = results.segments[i].conditions.energy.power[:,0] 
        Thrust = results.segments[i].conditions.frames.body.thrust_force_vector[:,0]
        Lift   = -results.segments[i].conditions.frames.wind.lift_force_vector[:,2]
        Drag   = -results.segments[i].conditions.frames.wind.drag_force_vector[:,0]
        
                       
        segment_tag  =  results.segments[i].tag
        segment_name = segment_tag.replace('_', ' ')
        
        # power 
        axes_1 = plt.subplot(2,2,1)
        axes_1.set_ylabel(r'Power (MW)')
        axes_1.plot(time,Power/1E6, color = line_colors[i], marker = ps.marker, linewidth = ps.line_width, label = segment_name) 
        set_axes(axes_1)                
        
        axes_2 = plt.subplot(2,2,2)
        axes_2.plot(time, Thrust/1000, color = line_colors[i], marker = ps.marker, linewidth = ps.line_width) 
        axes_2.set_ylabel(r'Thrust (kN)')
        set_axes(axes_2) 

        axes_3 = plt.subplot(2,2,3)
        axes_3.plot(time, Lift/1000, color = line_colors[i], marker = ps.marker, linewidth = ps.line_width)
        axes_3.set_xlabel('Time (mins)')
        axes_3.set_ylabel(r'Lift (kN)')
        set_axes(axes_3) 
        
        axes_4 = plt.subplot(2,2,4)
        axes_4.plot(time,Drag/1000 , color = line_colors[i], marker = ps.marker, linewidth = ps.line_width)
        axes_4.set_xlabel('Time (mins)')
        axes_4.set_ylabel(r'Drag (kN)')
        set_axes(axes_4)  
        
 
    if show_legend:    
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 5) 
        leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
    
    # Adjusting the sub-plots for legend 
    fig.subplots_adjust(top=0.8)
    
    # set title of plot 
    title_text    = 'Aerodynamic Forces'      
    fig.suptitle(title_text)
    
    if save_figure:
        plt.savefig(save_filename + file_type)   
    return
