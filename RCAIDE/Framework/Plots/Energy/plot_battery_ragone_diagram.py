# RCAIDE/Library/Plots/Energy/plot_battery_ragone_diagram.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  

from RCAIDE.Framework.Core import Units
from RCAIDE.Framework.Plots.Common import set_axes, plot_style
import matplotlib.pyplot as plt
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------   
def plot_battery_ragone_diagram(battery,
                          save_figure   = False, 
                          save_filename = "Ragone_Plot",
                          file_type     =  ".png",
                          width = 12, height = 7):
    """Plots the pack-level conditions of the battery throughout flight.

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
      
    fig   = plt.figure(save_filename)
    fig.set_size_inches(width,height)  
        
    axis_1 = plt.subplot(1,1,1)
    esp_plot = np.linspace(battery.ragone.lower_bound, battery.ragone.upper_bound,50)
    psp_plot = battery.ragone.const_1*10**(esp_plot*battery.ragone.const_2)
    axis_1.plot(esp_plot/(Units.Wh/Units.kg),psp_plot/(Units.kW/Units.kg), color = 'black', marker = ps.markers[0], linewidth = ps.line_width, label= battery.tag) 
    axis_1.set_ylabel('Specific Power (kW/kg)')
    axis_1.set_xlabel('Specific Energy (W-h/kg)')
    set_axes(axis_1)       
     
    # set title of plot 
    title_text    = 'Battery Ragone Plot'      
    fig.suptitle(title_text)
    
    if save_figure:
        plt.savefig(save_filename + file_type)   
    return  fig 