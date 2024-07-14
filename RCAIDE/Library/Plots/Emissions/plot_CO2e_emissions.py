# RCAIDE/Library/Plots/Emissions/plot_CO2e_emissions
# 
# 
# Created:  Jul 2024, M. Clarke

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
## @ingroup Library-Plots-Performance-Emissions 
def plot_CO2e_emissions(results,
                             save_figure = False,
                             show_legend = True,
                             save_filename = "CO2e_Emissions" ,
                             file_type = ".png",
                             width = 12, height = 7):
    """  
 
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

    line_colors   = cm.inferno(np.linspace(0,0.9,len(results.segments)))
    
    cum_y0  = 0
    cum_y1  = 0 
    cum_y1_0 = 0  
    
    for i in range(len(results.segments)): 
        time                = results.segments[i].conditions.frames.inertial.time[:, 0] / Units.min 
        emissions_CO2       = results.segments[i].conditions.emissions.total.CO2[:, 0]  
        emissions_NOx       = results.segments[i].conditions.emissions.total.NOx[:, 0] 
        emissions_H2O       = results.segments[i].conditions.emissions.total.H2O[:, 0] 
        emissions_Contrails = results.segments[i].conditions.emissions.total.Contrails[:, 0]
        emissions_Soot      = results.segments[i].conditions.emissions.total.Soot[:, 0]
        emissions_SO2       = results.segments[i].conditions.emissions.total.SO2[:, 0]  

        cum_y0 = np.zeros_like(emissions_CO2)  
        cum_y1 = cum_y1_0 + emissions_CO2 +  emissions_NOx  + emissions_H2O  + emissions_Contrails +  emissions_Soot +  emissions_SO2    

        segment_tag  =  results.segments[i].tag
        segment_name = segment_tag.replace('_', ' ')    
        axis_1.fill_between(time, cum_y0, cum_y1, where=(cum_y0 < cum_y1), color= line_colors[i],  interpolate=True, label = segment_name)   
        cum_y1_0 = cum_y1[-1] 
                
        axis_1.set_ylabel(r'CO2e Emissions (kg)') 
        set_axes(axis_1)
        
    if show_legend:
        leg =  fig.legend(bbox_to_anchor=(0.5, 0.95), loc='upper center', ncol = 5) 
        leg.set_title('Flight Segment', prop={'size': ps.legend_font_size, 'weight': 'heavy'})    
    
    # Adjusting the sub-plots for legend 
    fig.subplots_adjust(top=0.8)
    
    # set title of plot 
    title_text    = 'CO2e Emissions'      
    fig.suptitle(title_text)
    
    if save_figure:
        plt.savefig(save_filename + file_type)   
    return fig 