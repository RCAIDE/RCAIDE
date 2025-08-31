# Regression/scripts/Tests/load_diagram_test.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
import RCAIDE
from RCAIDE.Framework.Core import Units , Container
from RCAIDE.Library.Methods.Performance.aircraft_loading_diagram        import aircraft_loading_diagram

# python imports     
import numpy as np  
import sys
import matplotlib.pyplot as plt  
import os
# local imports 
sys.path.append(os.path.join( os.path.split(os.path.split(sys.path[0])[0])[0], 'Vehicles'))
from Embraer_190    import vehicle_setup as E190_vehicle_setup       

# ----------------------------------------------------------------------------------------------------------------------
#  REGRESSION
# ----------------------------------------------------------------------------------------------------------------------  
def main():
    
    vehicle    = E190_vehicle_setup()
 
    #  Weights Analysis
    weights = RCAIDE.Framework.Analyses.Weights.Conventional() 
    weights.settings.FLOPS.fidelity = 'Complex'  
 
    #  Aerodynamics Analysis 
    aerodynamics          = RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method()

    aerodynamics          = RCAIDE.Framework.Analyses.Aerodynamics.Vortex_Lattice_Method()        
    
    load_data =  aircraft_loading_diagram(vehicle,
                                          aerodynamic_analysis=aerodynamics,
                                          weights_analysis=weights, 
                                          altitude = 35000*Units.feet, 
                                          airspeed =450 * Units['knots'])
 
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
    y_pts_1  = weight[0, :]  
    y_pts_2  = weight[0, -1]  -  weight[0, :]  
    axis.plot( aerodynamic_moment[:,0], y_pts_1, 'go-')
    axis.plot( aerodynamic_moment[:,0], y_pts_2, 'go-')
    
    # payload loading line
    y_pts_3  = weight[:, 0]  
    y_pts_4  = weight[-1, 0]   -  weight[:, 0]  
    axis.plot( aerodynamic_moment[0, :], y_pts_3, 'bo-')
    axis.plot( aerodynamic_moment[0, :], y_pts_4, 'bo-')
    
    
    # Maximum Takeoff Weight line
    x_pts_MTOW = np.linspace(0, 1E8)
    y_pts_MTOW = np.ones_like(x_pts_MTOW)  *MTOW
    axis.plot(x_pts_MTOW, y_pts_MTOW, 'bo-') 
    
    
    # Maximum Landing Weight line
    x_pts_MLW = np.linspace(0, 1E8)
    y_pts_MLW = np.ones_like(x_pts_MLW)  *MLW
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