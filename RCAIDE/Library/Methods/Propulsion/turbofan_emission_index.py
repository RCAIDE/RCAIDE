## @ingroup Methods-Propulsion
# turbofan_emission_index.py
# 
# Created:  Sep 2015, M. Vegh
# Modified: Feb 2016, E. Botero
#           Oct 2017, E. Botero (major change/rename from turbofan_nox_emission_index.py, which was removed)

# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------

import numpy as np
from Legacy.trunk.S.Core import Data, Units

# ----------------------------------------------------------------------
#   turbofan_emission_index
# ----------------------------------------------------------------------


## @ingroup Methods-Propulsion
def func_turbofan_emission_index(turbofan, state):
    """
    Outputs a turbofan's emission_index takens from a regression calculated
    from NASA's Engine Performance Program (NEPP)
    
    Inputs:
    turbofan.
      combustor.
        inputs.
          stagnation_pressure     [Pa]
          stagnation_temperature  [K]
        outputs.
          stagnation_temperature  [K]
          
    Outputs:      
    emission.
          total.
                NOx               [kg]
                CO2               [kg]
                H2O               [kg]
                SO2               [kg]
          index.
                NOx               [kg/kg]
                CO2               [kg/kg]
                H2O               [kg/kg]
                SO2               [kg/kg]
    
    Source: Antoine, Nicholas, Aircraft Optimization for Minimal Environmental Impact, pp. 31 (PhD Thesis)
    
    
    """
    
    results = turbofan(state)
    p3      = turbofan.combustor.inputs.stagnation_pressure/Units.psi
    T3      = turbofan.combustor.inputs.stagnation_temperature/Units.degR 
    T4      = turbofan.combustor.outputs.stagnation_temperature/Units.degR
    mdot    = state.conditions.weights.vehicle_mass_rate
    I       = state.numerics.time.integrate
    
    NOx = .004194*T4*((p3/439.)**.37)*np.exp((T3-1471.)/345.)
    CO2 = 3.155  # This is in kg/kg
    H2O = 1.240  # This is in kg/kg 
    SO2 = 0.0008 # This is in kg/kg 
    
    #correlation in g Nox/kg fuel; convert to kg Nox/kg
    NOx = NOx * (Units.g/Units.kg) 
    
    # Integrate them over the entire segment
    NOx_total = np.dot(I,mdot*NOx)
    CO2_total = np.dot(I,mdot*CO2)
    SO2_total = np.dot(I,mdot*SO2)
    H2O_total = np.dot(I,mdot*H2O)

    emission = Data()
    emission.total = Data()
    emission.index = Data()
    emission.total.NOx = NOx_total
    emission.total.CO2 = CO2_total
    emission.total.H2O = H2O_total
    emission.total.SO2 = SO2_total 
    emission.index.NOx = NOx
    emission.index.CO2 = CO2
    emission.index.H2O = H2O
    emission.index.SO2 = SO2
    
    
    return emission


def turbofan_emission_index(State, Settings, System):
	#TODO: turbofan = [Replace With State, Settings, or System Attribute]
	#TODO: state    = [Replace With State, Settings, or System Attribute]

	results = func_turbofan_emission_index('turbofan', 'state')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System