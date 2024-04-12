## @ingroup Methods-Power-Battery-Variable_Mass 
# find_total_mass_gain.py
# 
# Created:  ### 2104, M. Vegh
# Modified: Feb 2016, E. Botero

# ----------------------------------------------------------------------
#  Find Total Mass Gain
# ----------------------------------------------------------------------
## @ingroup Methods-Power-Battery-Variable_Mass 
def func_find_total_mass_gain(battery):
    """finds the total mass of air that the battery 
    accumulates when discharged fully
    
    Assumptions:
    Earth Atmospheric composition
    
    Inputs:
    battery.max_energy [J]
    battery.
      mass_gain_factor [kg/W]
      
    Outputs:
      mdot             [kg]
    """
    
    
    
    
    mgain=battery.max_energy*battery.mass_gain_factor
    
    return mgain


find_total_mass_gain(State, Settings, System):
	#TODO: battery = [Replace With State, Settings, or System Attribute]

	results = func_find_total_mass_gain('battery',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System