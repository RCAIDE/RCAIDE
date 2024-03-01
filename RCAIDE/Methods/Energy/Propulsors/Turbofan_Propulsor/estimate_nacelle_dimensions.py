## @ingroup Methods-Energy-Propulsors-Turbofan_Propulsor
# RCAIDE/Methods/Energy/Propulsors/Turbofan_Propulsor/estimate_nacelle_dimensions.py
# 
# 
# Created:  Feb 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports  
from RCAIDE.Core      import Units 

# Python package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  estimate_nacelle_dimensions
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Energy-Propulsors-Turbofan_Propulsor
def estimate_nacelle_dimensions(turbofan, nacelle):
    """Estimates the size of nacelle given turbofan properties and rewrites 
    nacelle geometry parameters.
    
    Assumptions:

    Source:
    http://adg.stanford.edu/aa241/AircraftDesign.html

    Inputs:
    turbofan.sealevel_static_thrust [N]

    Outputs:
       nacelle.diameter             [m]
       areas.wetted                 [m^2]
    turbofan.   
       engine_length                [m] 

    Properties Used:
    N/A
    """    

    #unpack
    slsthrust                 = turbofan.sealevel_static_thrust / Units.lbf # convert from N to lbs. in correlation

    #based on 241 notes
    nacelle_diameter_in       = 1.0827*slsthrust**0.4134
    nacelle.diameter          = 0.0254*nacelle_diameter_in 
    
    # compute other dimensions based on AA241 notes
    L_eng_in                  = 2.4077*slsthrust**0.3876
    L_eng_m                   = L_eng_in * Units.inches        # engine length in metres 

    # pack 
    turbofan.engine_length    = L_eng_m
    turbofan.inlet_diameter   = nacelle.diameter/np.sqrt(2.1) 
    nacelle.inlet_diameter    = nacelle.diameter/np.sqrt(2.1) 
    nacelle.areas.wetted      = 1.1*np.pi*nacelle.diameter*L_eng_m
    
    return  