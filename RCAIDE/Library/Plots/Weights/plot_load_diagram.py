# RCAIDE/Library/Plots/Weights/plot_load_diagram.py
# 
# 
# Created:  Aug 2025, M. Clarke

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
def plot_load_diagram(results):
    
    # get plotting style 
    ps      = plot_style()  

    parameters = {'axes.labelsize': ps.axis_font_size,
                  'xtick.labelsize': ps.axis_font_size,
                  'ytick.labelsize': ps.axis_font_size,
                  'axes.titlesize': ps.title_font_size}
    plt.rcParams.update(parameters)

    fig  = plt.figure('Aircraft Loading Dragram')
    axis = fig.add_subplot(1,1,1)
    
    min_range = 0
    max_range = 0
    
    # ------------------------------------------------------------------------
    # fuel loading line
    # ------------------------------------------------------------------------
    fuel_weight          = results.weight[0, :]
    fuel_moment_forward  = results.aerodynamic_moment[0, :]  
    axis.plot( fuel_moment_forward, fuel_weight, 'go-', linewidth=3, label = "Fuel")
    min_range =  np.minimum( min(fuel_moment_forward), min_range)
    max_range =  np.maximum( max(fuel_moment_forward), max_range)

    # ------------------------------------------------------------------------    
    # payload loading line
    # ------------------------------------------------------------------------

    payload_weight          = results.weight[:, 0]
    payload_moment_forward  = results.aerodynamic_moment[:, 0] 
    axis.plot( payload_moment_forward, payload_weight, 'bo-', linewidth=3, label = "Payload") 
    min_range =  np.minimum( min(payload_moment_forward), min_range)
    max_range =  np.maximum( max(payload_moment_forward), max_range)

    # ------------------------------------------------------------------------    
    # cumulative
    # ------------------------------------------------------------------------
    y_pts_5  = np.hstack((payload_weight,  results.weight[-1, :][1:]) ) 
    x_pts_5  = np.hstack((payload_moment_forward,  results.aerodynamic_moment[-1, :][1:] ))

    y_pts_6  = np.hstack((fuel_weight,  results.weight[:, -1][1:]) ) 
    x_pts_6  = np.hstack((fuel_moment_forward,  results.aerodynamic_moment[:, -1][1:] ))
    
    axis.plot( x_pts_5, y_pts_5, 'r-')
    axis.plot( x_pts_6, y_pts_6, 'r-') 
    
    min_range =  np.minimum( min(x_pts_5), min_range)
    max_range =  np.maximum( max(x_pts_5), max_range)

    # ------------------------------------------------------------------------    
    # Maximum Takeoff Weight line
    # ------------------------------------------------------------------------
    x_pts_MTOW = np.linspace(min_range, max_range)
    y_pts_MTOW = np.ones_like(x_pts_MTOW)  * results.MTOW
    axis.plot(x_pts_MTOW, y_pts_MTOW, 'k-', label = 'MTOW') 
    

    # ------------------------------------------------------------------------    
    # Maximum Landing Weight line
    # ------------------------------------------------------------------------
    x_pts_MLW = x_pts_MTOW
    y_pts_MLW = np.ones_like(x_pts_MLW)  * results.MLW
    axis.plot(x_pts_MLW, y_pts_MLW, 'k--', label = 'MLW') 
    
    n = results.number_of_points
    x = np.array(results.aero_weight).resultshape(n*n, n)
    y = np.array(results.aero_moment).resultshape(n*n, n)
    z = np.array(results.aero_static_margin).resultshape(n*n, n) 
     
    axis.contourf(y, x, z) 
    #fig.colorbar(cntr1, ax=axis)  
     
    axis.legend(loc='upper right')
    axis.set_xlabel('Moment')
    axis.set_ylabel('Weight') 
    set_axes(axis) 
    fig.tight_layout()       
                                  
    return