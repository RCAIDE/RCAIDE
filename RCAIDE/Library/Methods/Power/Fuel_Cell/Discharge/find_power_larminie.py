## @ingroup Methods-Power-Fuel_Cell-Discharge
# find_power_larminie.py
#
# Created : Apr 2015, M. Vegh 
# Modified: Sep 2015, M. Vegh
#           Feb 2016, E. Botero

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import numpy as np
from Legacy.trunk.S.Core import Units
from .find_voltage_larminie import find_voltage_larminie

# ----------------------------------------------------------------------
#  Find Power Larminie
# ----------------------------------------------------------------------

## @ingroup Methods-Power-Fuel_Cell-Discharge
def func_find_power_larminie(current_density, fuel_cell, sign=1.0):
    '''
    Function that determines the power output per cell, based on in 
    input current density
    
    Assumptions:
    None(calls other functions)
    
    Inputs:
    current_density      [Amps/m**2]
    fuel cell.
        interface area   [m**2]
        
    Outputs:
    power_out            [W]
    
    '''
    
    # sign variable is used so that you can maximize the power, by minimizing the -power
    i1            = current_density
    A             = fuel_cell.interface_area
    v             = find_voltage_larminie(fuel_cell,current_density)  #useful voltage vector
    power_out     = sign* np.multiply(v,i1)*A       #obtain power output in W/cell
    
    #want to minimize
    return power_out


find_power_larminie(State, Settings, System):
	#TODO: current_density = [Replace With State, Settings, or System Attribute]
	#TODO: fuel_cell       = [Replace With State, Settings, or System Attribute]
	#TODO: sign            = [Replace With State, Settings, or System Attribute]

	results = func_find_power_larminie('current_density', 'fuel_cell', 'sign')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System