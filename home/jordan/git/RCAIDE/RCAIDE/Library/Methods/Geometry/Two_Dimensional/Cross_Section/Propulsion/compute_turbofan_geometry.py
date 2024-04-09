## @ingroup Methods-Geometry-Two_Dimensional-Cross_Section-Propulsion
# compute_turbofan_geometry.py
#
# Created:  Jun 2015, A. Variyar 
# Modified: Mar 2016, M. Vegh
#           Apr 2021, E. Botero

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from Legacy.trunk.S.Core import Units

# package imports
import numpy as np

# ----------------------------------------------------------------------
#  Correlation-based methods to compute engine geometry
# ----------------------------------------------------------------------

## @ingroup Methods-Geometry-Two_Dimensional-Cross_Section-Propulsion
def func_compute_turbofan_geometry(turbofan, nacelle):
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
    slsthrust         = turbofan.sealevel_static_thrust / Units.lbf # convert from N to lbs. in correlation

    #based on 241 notes
    nacelle_diameter_in  = 1.0827*slsthrust**0.4134
    nacelle.diameter     = 0.0254*nacelle_diameter_in

    
    #compute other dimensions based on AA241 notes
    L_eng_in          = 2.4077*slsthrust**0.3876
    L_eng_m           = L_eng_in * Units.inches        # engine length in metres 

    # pack 
    turbofan.engine_length    = L_eng_m
    turbofan.inlet_diameter   = nacelle.diameter/np.sqrt(2.1) 
    nacelle.inlet_diameter    = nacelle.diameter/np.sqrt(2.1) 
    nacelle.areas.wetted      = 1.1*np.pi*nacelle.diameter*L_eng_m
    
    return turbofan , nacelle


def compute_turbofan_geometry(State, Settings, System):
	#TODO: turbofan = [Replace With State, Settings, or System Attribute]
	#TODO: nacelle  = [Replace With State, Settings, or System Attribute]

	results = func_compute_turbofan_geometry('turbofan', 'nacelle')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System