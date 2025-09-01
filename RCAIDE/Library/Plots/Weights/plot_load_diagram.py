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
from scipy.spatial import ConvexHull
from shapely.geometry import Polygon
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
    n = results.number_of_points
    
    # ------------------------------------------------------------------------
    # fuel loading line
    # ------------------------------------------------------------------------
    fuel_mass            = results.mass[0, :]
    fuel_moment_forward  = results.aerodynamic_moment[0, :]  
    #axis.plot( fuel_moment_forward, fuel_mass, 'go-', linewidth=3, label = "Fuel")
    min_range =  np.minimum( min(fuel_moment_forward), min_range)
    max_range =  np.maximum( max(fuel_moment_forward), max_range)

    # ------------------------------------------------------------------------    
    # payload loading line
    # ------------------------------------------------------------------------ 
    payload_mass          = results.mass[:, 0] 
    payload_moment_forward  = results.aerodynamic_moment[:, 0] 
    #axis.plot( payload_moment_forward, payload_mass, 'bo-', linewidth=3, label = "Payload") 
    min_range =  np.minimum( min(payload_moment_forward), min_range)
    max_range =  np.maximum( max(payload_moment_forward), max_range)

    # ------------------------------------------------------------------------    
    # cumulative
    # ------------------------------------------------------------------------ 
    
    # 1. Generate sample scattered data 
    points =  np.hstack((   np.atleast_2d(results.aerodynamic_moment.flatten()).T,  np.atleast_2d(results.mass.flatten()).T ))
    
    # 2. Compute the convex hull
    hull = ConvexHull(points)
    
    # 3. Extract the vertices of the hull in a counter-clockwise order
    hull_points = points[hull.vertices]
    
    # 4. Create a Shapely Polygon from the hull vertices
    # The vertices are already ordered, but Shapely can handle it
    polygon = Polygon(hull_points) 
    
    # Plot the convex hull polygon boundary
    x_hull, y_hull = polygon.exterior.xy
    
    axis.fill(x_hull, y_hull, color='grey', alpha=0.3, edgecolor='black', linewidth=2)
    axis.plot(x_hull, y_hull, 'k-')

    # ------------------------------------------------------------------------    
    # Maximum Takeoff Weight line
    # ------------------------------------------------------------------------
    x_pts_MTOW = np.linspace(min_range, max_range)
    y_pts_MTOW = np.ones_like(x_pts_MTOW)  * results.MTOW
    axis.plot(x_pts_MTOW, y_pts_MTOW, 'r-', label = 'MTOW') 
    

    # ------------------------------------------------------------------------    
    # Maximum Landing Weight line
    # ------------------------------------------------------------------------
    x_pts_MLW = x_pts_MTOW
    y_pts_MLW = np.ones_like(x_pts_MLW)  * results.MLW
    axis.plot(x_pts_MLW, y_pts_MLW, 'r--', label = 'MLW') 
    

    # ------------------------------------------------------------------------    
    # Maximum Landing Weight line
    # ------------------------------------------------------------------------    
    #n = results.number_of_points
    #x = np.array(results.aero_mass).resultshape(n*n, n)
    #y = np.array(results.aero_moment).resultshape(n*n, n)
    #z = np.array(results.aero_static_margin).resultshape(n*n, n) 
     
    #axis.contourf(y, x, z) 
    ##fig.colorbar(cntr1, ax=axis)  
     
     

    # ------------------------------------------------------------------------    
    # Axis Items
    # ------------------------------------------------------------------------        
    axis.legend(loc='upper right')
    axis.set_xlabel(r'$X_{CG}$ (%MAC)')
    axis.set_ylabel('Weight')
    axis.set_xticklabels([])
    #set_axes(axis)
    axis.grid(True)
    axis.xaxis.grid(False)
    fig.tight_layout()       
                                  
    return