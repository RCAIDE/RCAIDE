## @ingroup Library-Plots-Geometry
# RCAIDE/Library/Plots/Geometry/plot_airfoil.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
# RCAIDE imports 
from RCAIDE.Library.Plots.Common import plot_style
from RCAIDE.Library.Methods.Geometry.Airfoil  import import_airfoil_geometry  

# package imports 
import matplotlib.pyplot as plt 

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Plots-Geometry
def plot_airfoil(airfoil_paths,
                 save_figure = False, 
                 save_filename = "Airfoil_Geometry",
                 file_type = ".png", 
                 width = 12, height = 7):
    """This plots all airfoil defined in the list "airfoil_names" 

    Assumptions:
    None

    Source:
    None

    Inputs:
    airfoil_geometry_files   <list of strings>

    Outputs: 
    Plots

    Properties Used:
    N/A	
    """
    # get airfoil coordinate geometry     
    airfoil_geometry = import_airfoil_geometry(airfoil_paths)

    # get plotting style 
    ps      = plot_style()  

    parameters = {'axes.labelsize': ps.axis_font_size,
                  'xtick.labelsize': ps.axis_font_size,
                  'ytick.labelsize': ps.axis_font_size,
                  'axes.titlesize': ps.title_font_size}
    plt.rcParams.update(parameters)    

    fig  = plt.figure(save_filename)
    fig.set_size_inches(width,height) 
    axis = fig.add_subplot(1,1,1)     
    axis.plot(airfoil_geometry.x_coordinates,airfoil_geometry.y_coordinates, color = ps.color, marker = ps.markers[0], linewidth = ps.line_width) 
    axis.set_xlabel('x')
    axis.set_ylabel('y')    
     
    if save_figure:
        fig.savefig(save_filename.replace("_", " ") + file_type)  
     
    return fig
