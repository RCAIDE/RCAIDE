# RCAIDE/Visualization/Performance/Energy/Battery/plot_battery_ragone_diagram.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  

from RCAIDE.Core import Units
from RCAIDE.Visualization.Performance.Common import set_axes, plot_style
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np  

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Visualization-Performance-Energy-Battery
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
      
    fig   = plt.figure(save_filename)
    fig.set_size_inches(width,height)  
        
    axes_1 = plt.subplot(1,1,1)
    esp_plot = np.linspace(battery.ragone.lower_bound, battery.ragone.upper_bound,50)
    psp_plot = battery.ragone.const_1*10**(esp_plot*battery.ragone.const_2)
    axes_1.plot(esp_plot/(Units.Wh/Units.kg),psp_plot/(Units.kW/Units.kg), color = 'black', marker = ps.marker, linewidth = ps.line_width, label= battery.tag) 
    axes_1.set_ylabel('Specific Power (kW/kg)')
    axes_1.set_xlabel('Specific Energy (W-h/kg)')
    set_axes(axes_1)       
     
    # set title of plot 
    title_text    = 'Battery Ragone Plot'      
    fig.suptitle(title_text)
    
    if save_figure:
        plt.savefig(save_filename + file_type)   
    return 