# RCAIDE/Library/Plots/Energy/plot_altitude_sfc_weight.py
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
def plot_propulsor_throttles(results,
                             save_figure = False,
                             show_legend = True,
                             save_filename = "Propulsor_Throttles" ,
                             file_type = ".png",
                             width = 12, height = 7):
    """This plots the altitude, specific fuel consumption and vehicle weight.

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
     
    # get line colors for plots 
    line_colors   = cm.inferno(np.linspace(0,0.9,len(results.segments)))      
     
    fig   = plt.figure(save_filename)
    fig.set_size_inches(width,height)
    
    for i, segment in enumerate(results.segments):
        time     = segment.conditions.frames.inertial.time[:, 0] / Units.min  
        segment_tag  =  segment.tag
        segment_name = segment_tag.replace('_', ' ') 
        
        # power 
        axis_1 = plt.subplot(1,1,1)
        axis_1.set_ylabel(r'Throttle')
        set_axes(axis_1)  
        for network in segment.analyses.energy.vehicle.networks: 
            busses      = network.busses
            fuel_lines  = network.fuel_lines
            for bus in busses:
                for j ,  propulsor in enumerate(bus.propulsors):
                    if j == 0:
                        eta = segment.conditions.energy[bus.tag][propulsor.tag].throttle[:,0]  
                        axis_1.plot(time, eta, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width,  label = segment_name + ': '+ propulsor.tag ) 
                    elif bus.identical_propulsors == False  and j != 0:
                        eta = segment.conditions.energy[bus.tag][propulsor.tag].throttle[:,0]  
                        axis_1.plot(time, eta, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width,  label = segment_name + ': '+ propulsor.tag )        
            for fuel_line in fuel_lines:  
                for j ,  propulsor in enumerate(fuel_line.propulsors):
                    if j == 0:
                        eta = segment.conditions.energy[fuel_line.tag][propulsor.tag].throttle[:,0]  
                        axis_1.plot(time, eta, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width,  label = segment_name + ': '+ propulsor.tag )     
                    elif fuel_line.identical_propulsors == False  and j != 0: 
                        eta = segment.conditions.energy[fuel_line.tag][propulsor.tag].throttle[:,0]  
                        axis_1.plot(time, eta, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width,  label = segment_name + ': '+ propulsor.tag )      
    if show_legend:
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 5) 
        leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
    
    # Adjusting the sub-plots for legend 
    fig.subplots_adjust(top=0.8)
    
    # set title of plot 
    title_text    = 'Throttle'      
    fig.suptitle(title_text)
    
    if save_figure:
        plt.savefig(save_filename + file_type)   
    return fig 