## @ingroup Methods-Power-Fuel_Cell-Discharge
# find_voltage_larminie.py
#
# Created : Apr 2015, M. Vegh 
# Modified: Feb 2016, E. Botero
  
# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import numpy as np
from Legacy.trunk.S.Core import Units

# ----------------------------------------------------------------------
#  Find Voltage Larminie
# ----------------------------------------------------------------------

## @ingroup Methods-Power-Fuel_Cell-Discharge
def func_find_voltage_larminie(fuel_cell,current_density):
    '''
    function that determines the fuel cell voltage based on an input
    current density and some semi-empirical values to describe the voltage
    drop off with current
    
    Assumptions:
    voltage curve is a function of current density of the form
    v = Eoc-r*i1-A1*np.log(i1)-m*np.exp(n*i1)
    
    Inputs:
    current_density           [A/m**2]
    fuel_cell.
        r                     [Ohms*m**2]
        A1                    [V]
        m                     [V]
        n                     [m**2/A]
        Eoc                   [V]
   
    Outputs:
        V                     [V]
         
    
    '''
    r   = fuel_cell.r/(Units.kohm*(Units.cm**2))
    Eoc = fuel_cell.Eoc 
    A1  = fuel_cell.A1  
    m   = fuel_cell.m   
    n   = fuel_cell.n   
    
    i1 = current_density/(Units.mA/(Units.cm**2.)) #current density(mA cm^-2)
    v  = Eoc-r*i1-A1*np.log(i1)-m*np.exp(n*i1)     #useful voltage vector

    return v


def find_voltage_larminie(State, Settings, System):
	#TODO: fuel_cell       = [Replace With State, Settings, or System Attribute]
	#TODO: current_density = [Replace With State, Settings, or System Attribute]

	results = func_find_voltage_larminie('fuel_cell', 'current_density')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System