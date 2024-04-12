## @ingroup Methods-Power-Battery-Ragone
# find_ragone_optimimum.py
# 

# Created:  ### 2014, M. Vegh
# Modified: Sep 2015, M. Vegh
#           Feb 2016, E. Botero

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import scipy as sp
from .find_ragone_properties import find_ragone_properties

# ----------------------------------------------------------------------
#  Methods
# ----------------------------------------------------------------------
## @ingroup Methods-Power-Battery-Ragone
def func_find_ragone_optimum(battery, energy, power): #adds a battery that is optimized based on power and energy requirements and technology
    """
    Uses Brent's Bracketing Method to find an optimum-mass battery based on the 
    specific energy and specific power of the battery determined from the battery's ragone plot.
    
    Assumptions:
    Specific power can be modeled as a curve vs. specific energy of the form c1*10**(c2*specific_energy)
    
    Inputs:
    energy            [J]
    power             [W]
    battery.
      specific_energy [J/kg]               
      specific_power  [W/kg]
      ragone.
        constant_1    [W/kg]
        constant_2    [J/kg]
        upper_bound   [J/kg]
        lower_bound   [J/kg]
                
    Outputs:
    battery.
      specific_energy [J/kg]
      specific_power  [W/kg]
      mass_properties.
        mass           [kg]    
                
           

    Properties Used:
    N/A  
    """

    specific_energy_guess = battery.specific_energy
    
    lb = battery.ragone.lower_bound
    ub = battery.ragone.upper_bound

    #optimize!
    specific_energy_opt = sp.optimize.fminbound(find_ragone_properties, lb, ub, args=( battery, energy, power), xtol=1e-12)
    
    #now initialize the battery with the new optimum properties
    find_ragone_properties(specific_energy_opt, battery, energy, power)


def find_ragone_optimum(State, Settings, System):
	#TODO: battery = [Replace With State, Settings, or System Attribute]
	#TODO: energy  = [Replace With State, Settings, or System Attribute]
	#TODO: power   = [Replace With State, Settings, or System Attribute]

	results = func_find_ragone_optimum('battery', 'energy', 'power')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System