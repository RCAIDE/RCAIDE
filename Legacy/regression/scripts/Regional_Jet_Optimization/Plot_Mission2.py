# Plot_Mission.py
# 
# Created:  May 2015, E. Botero
# Modified: 

# ----------------------------------------------------------------------        
#   Imports
# ----------------------------------------------------------------------    

import Legacy.trunk.S as SUAVE
from Legacy.trunk.S.Core import Units
from Legacy.trunk.S.Plots.Performance.Mission_Plots import *  

# ----------------------------------------------------------------------
#   Plot Functions
# ----------------------------------------------------------------------

def plot_mission(results,line_style='bo-'):
    
    plot_altitude_sfc_weight(results, line_style) 
    
    plot_flight_conditions(results, line_style) 
    
    plot_aerodynamic_coefficients(results, line_style)  
    
    plot_aircraft_velocities(results, line_style)
    
    plot_drag_components(results, line_style)


    return
 