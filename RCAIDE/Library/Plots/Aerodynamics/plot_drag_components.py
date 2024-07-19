## @ingroup Library-Plots-Performance-Aerodynamics
# RCAIDE/Library/Plots/Performance/Aerodynamics/plot_drag_components.py
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
## @ingroup Library-Plots-Performance-Aerodynamics
def plot_drag_components(results,
                         save_figure=False,
                         show_legend= True,
                         save_filename="Drag_Components",
                         file_type=".png",
                        width = 12, height = 7):
    """This plots the drag components of the aircraft
    
    Assumptions:
    None
    
    Source:
    None
    
    Inputs:
    results.segments.condtions.aerodynamics.coefficients.drag
          parasite.total
          induced.total
          compressible.total
          miscellaneous.total
          
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
    axis_1 = plt.subplot(1,1,1)
    fig.set_size_inches(12,height)
    
    for i in range(len(results.segments)): 
        time   = results.segments[i].conditions.frames.inertial.time[:,0] / Units.min 
        drag   = results.segments[i].conditions.aerodynamics.coefficients.drag 
        cdp    = drag.parasite.total[:,0]
        cdi    = drag.induced.total[:,0]
        cdc    = drag.compressible.total[:,0]
        cdm    = drag.miscellaneous.total[:,0] 
        cd     = drag.total[:,0]  
        
        if i ==  0:
            axis_1.plot(time, cdp, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width, label = r'$C_{Dp}$') 
            axis_1.plot(time,cdi, color = line_colors[i], marker = ps.markers[1], linewidth = ps.line_width,  label = r'$C_{Di}$')  
            axis_1.plot(time, cdc, color = line_colors[i], marker = ps.markers[2], linewidth = ps.line_width,  label =r'$C_{Dc}$')  
            axis_1.plot(time, cdm, color = line_colors[i], marker = ps.markers[3], linewidth = ps.line_width,  label =r'$C_{Dm}$')  
            axis_1.plot(time, cd, color = line_colors[i], marker = ps.markers[5], linewidth = ps.line_width,  label =r'$C_D$')
        else:
            axis_1.plot(time, cdp, color = line_colors[i], marker = ps.markers[0], linewidth = ps.line_width)
            axis_1.plot(time,cdi, color = line_colors[i], marker = ps.markers[1], linewidth = ps.line_width)
            axis_1.plot(time, cdc, color = line_colors[i], marker = ps.markers[2], linewidth = ps.line_width)
            axis_1.plot(time, cdm, color = line_colors[i], marker = ps.markers[3], linewidth = ps.line_width) 
            axis_1.plot(time, cd, color = line_colors[i], marker = ps.markers[5], linewidth = ps.line_width)
    
        set_axes(axis_1)            
        axis_1.set_xlabel('Time (mins)')
        axis_1.set_ylabel('Drag Compoments') 
        
    
    if show_legend:                    
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 5) 
        leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
    
    # Adjusting the sub-plots for legend 
    fig.subplots_adjust(top=0.8)
    
    # set title of plot 
    title_text    = 'Drag Components'      
    fig.suptitle(title_text)
    
    if save_figure:
        plt.savefig(save_filename + file_type)   
    return fig 