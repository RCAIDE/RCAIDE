# Regression/scripts/Tests/load_diagram_test.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
import RCAIDE
from RCAIDE.Framework.Core import Units  
from RCAIDE.Library.Methods.Performance.aircraft_loading_diagram        import aircraft_loading_diagram
from RCAIDE.Library.Plots.Common import set_axes, plot_style

# python imports      
import os
import numpy as np  
import pickle
import sys 

# local imports 
sys.path.append(os.path.join( os.path.split(os.path.split(sys.path[0])[0])[0], 'Vehicles'))
from Embraer_190    import vehicle_setup as E190_vehicle_setup       

# ----------------------------------------------------------------------------------------------------------------------
#  REGRESSION
# ----------------------------------------------------------------------------------------------------------------------  
def main():
    
    vehicle    = E190_vehicle_setup()

    # take out control surfaces to make regression run faster
    for wing in vehicle.wings:
        wing.control_surfaces  = Container()
        
    #  Weights Analysis
    weights = RCAIDE.Framework.Analyses.Weights.Conventional() 
    weights.settings.FLOPS.fidelity = 'Complex'  
 
    #  Aerodynamics Analysis 
    aerodynamics          = RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method()
    aerodynamics.settings.number_of_spanwise_vortices   = 5
    aerodynamics.settings.number_of_chordwise_vortices  = 2  
    
    #  Stability Analysis
    stability     = RCAIDE.Framework.Analyses.Stability.Vortex_Lattice_Method()  
    stability.settings.number_of_spanwise_vortices   = 5
    stability.settings.number_of_chordwise_vortices  = 2        
    
    
    RES =  aircraft_loading_diagram(vehicle,
                                          aerodynamic_analysis=aerodynamics,
                                          weights_analysis=weights,
                                          stability_analysis=stability,
                                          altitude = 35000*Units.feet, 
                                          airspeed =450 * Units['knots'])
 
    plot_load_diagram(RES)
        
    return

def plot_load_diagram(RES):
    
    # get plotting style 
    ps      = plot_style()  

    parameters = {'axes.labelsize': ps.axis_font_size,
                  'xtick.labelsize': ps.axis_font_size,
                  'ytick.labelsize': ps.axis_font_size,
                  'axes.titlesize': ps.title_font_size}
    plt.rcParams.update(parameters)

    fig  = plt.figure('Aircraft Loading Dragram')
    axis = fig.add_subplot(1,1,1)
    
    # fuel loading line
    y_pts_1  = RES.weight[0, :]  
    y_pts_2  = RES.weight[0, -1]  -  RES.weight[0, :]  
    axis.plot( RES.aerodynamic_moment[:,0], y_pts_1, 'go-')
    axis.plot( RES.aerodynamic_moment[:,0], y_pts_2, 'go-')
    
    # payload loading line
    y_pts_3  = RES.weight[:, 0]  
    y_pts_4  = RES.weight[-1, 0]   -  RES.weight[:, 0]  
    axis.plot( RES.aerodynamic_moment[0, :], y_pts_3, 'bo-')
    axis.plot( RES.aerodynamic_moment[0, :], y_pts_4, 'bo-')
    
    
    # Maximum Takeoff Weight line
    x_pts_MTOW = np.linspace(0, 1E8)
    y_pts_MTOW = np.ones_like(x_pts_MTOW)  * RES.MTOW
    axis.plot(x_pts_MTOW, y_pts_MTOW, 'bo-') 
    
    
    # Maximum Landing Weight line
    x_pts_MLW = np.linspace(0, 1E8)
    y_pts_MLW = np.ones_like(x_pts_MLW)  * RES.MLW
    axis.plot(x_pts_MLW, y_pts_MLW, 'bo-') 
    
    
    # Aerodynamics Lines 
      
    #ngridx = 100
    #ngridy = 200
    #x = np.array(aero_weight) 
    #y = np.array(aero_moment)
    #z = np.array(aero_static_margin) 
    
    ## Create grid values first.
    #xi = np.linspace(-2.1, 2.1, ngridx)
    #yi = np.linspace(-2.1, 2.1, ngridy)
    
    ## Linearly interpolate the data (x, y) on a grid defined by (xi, yi).
    #triang       = tri.Triangulation(x, y)
    #interpolator = tri.LinearTriInterpolator(triang, z)
    #Xi, Yi       = np.meshgrid(xi, yi)
    #zi           = interpolator(Xi, Yi)
     
    #axis.contour(xi, yi, zi, levels=14, linewidths=0.5, colors='k')
    #cntr1  = axis.contourf(xi, yi, zi, levels=14, cmap="RdBu_r") 
    #fig.colorbar(cntr1, ax=axis) 
    #axis.set(xlim=(-2, 2), ylim=(-2, 2)) 
     

    axis.set_xlabel('Moment')
    axis.set_ylabel('Weight') 
    set_axes(axis) 
    fig.tight_layout()       
                                  
    return
 
 
if __name__ == '__main__': 
    main()  