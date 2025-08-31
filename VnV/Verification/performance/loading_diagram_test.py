# Regression/scripts/Tests/load_diagram_test.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports  
import RCAIDE
from RCAIDE.Framework.Core import Units  , Container
from RCAIDE.Library.Methods.Performance.aircraft_loading_diagram        import aircraft_loading_diagram
from RCAIDE.Library.Plots.Common import set_axes, plot_style
import matplotlib.pyplot as plt
import matplotlib.tri as tri

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
    
    new_sim = False
    
    if new_sim:
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
        
        save_data(RES,'loading_results')
    else:
        
        RES = load_data('loading_results')
 
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
    
    min_range = 0
    max_range = 0
    
    # ------------------------------------------------------------------------
    # fuel loading line
    # ------------------------------------------------------------------------
    fuel_weight          = RES.weight[0, :]
    fuel_moment_forward  = RES.aerodynamic_moment[0, :]  
    axis.plot( fuel_moment_forward, fuel_weight, 'go-', linewidth=3, label = "Fuel")
    min_range =  np.minimum( min(fuel_moment_forward), min_range)
    max_range =  np.maximum( max(fuel_moment_forward), max_range)

    # ------------------------------------------------------------------------    
    # payload loading line
    # ------------------------------------------------------------------------

    payload_weight          = RES.weight[:, 0]
    payload_moment_forward  = RES.aerodynamic_moment[:, 0] 
    axis.plot( payload_moment_forward, payload_weight, 'bo-', linewidth=3, label = "Payload") 
    min_range =  np.minimum( min(payload_moment_forward), min_range)
    max_range =  np.maximum( max(payload_moment_forward), max_range)

    # ------------------------------------------------------------------------    
    # cumulative
    # ------------------------------------------------------------------------
    y_pts_5  = np.hstack((payload_weight,  RES.weight[-1, :][1:]) ) 
    x_pts_5  = np.hstack((payload_moment_forward,  RES.aerodynamic_moment[-1, :][1:] ))

    y_pts_6  = np.hstack((fuel_weight,  RES.weight[:, -1][1:]) ) 
    x_pts_6  = np.hstack((fuel_moment_forward,  RES.aerodynamic_moment[:, -1][1:] ))
    
    axis.plot( x_pts_5, y_pts_5, 'r-')
    axis.plot( x_pts_6, y_pts_6, 'r-') 
    
    min_range =  np.minimum( min(x_pts_5), min_range)
    max_range =  np.maximum( max(x_pts_5), max_range)

    # ------------------------------------------------------------------------    
    # Maximum Takeoff Weight line
    # ------------------------------------------------------------------------
    x_pts_MTOW = np.linspace(min_range, max_range)
    y_pts_MTOW = np.ones_like(x_pts_MTOW)  * RES.MTOW
    axis.plot(x_pts_MTOW, y_pts_MTOW, 'k-', label = 'MTOW') 
    

    # ------------------------------------------------------------------------    
    # Maximum Landing Weight line
    # ------------------------------------------------------------------------
    x_pts_MLW = x_pts_MTOW
    y_pts_MLW = np.ones_like(x_pts_MLW)  * RES.MLW
    axis.plot(x_pts_MLW, y_pts_MLW, 'k--', label = 'MLW') 
    
    resolution = 4
    x = np.array(RES.aero_weight).reshape(resolution*resolution, resolution)
    y = np.array(RES.aero_moment).reshape(resolution*resolution, resolution)
    z = np.array(RES.aero_static_margin).reshape(resolution*resolution, resolution) 
     
    axis.contourf(x, y, z) 
    #fig.colorbar(cntr1, ax=axis)  
     
    axis.legend(loc='upper right')
    axis.set_xlabel('Moment')
    axis.set_ylabel('Weight') 
    set_axes(axis) 
    fig.tight_layout()       
                                  
    return

def save_data(data,filename): 
    pickle_file  = filename + '.pkl'
    with open(pickle_file, 'wb') as file:
        pickle.dump(data, file) 
    return 


def load_data(filename):  
    load_file = filename + '.pkl' 
    with open(load_file, 'rb') as file:
        results = pickle.load(file) 
    return results
 

 
if __name__ == '__main__': 
    main()
    plt.show()