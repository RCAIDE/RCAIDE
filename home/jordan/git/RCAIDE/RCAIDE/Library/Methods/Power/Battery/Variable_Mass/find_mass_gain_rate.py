## @ingroup Methods-Power-Battery-Variable_Mass 
# find_mass_gain_rate.py
# 
# Created:  ### 2104, M. Vegh
# Modified: Feb 2016, E. Botero

# ----------------------------------------------------------------------
#  Find Mass Gain Rate
# ----------------------------------------------------------------------
## @ingroup Methods-Power-Battery-Variable_Mass 
def func_find_mass_gain_rate(battery,power):
    """finds the mass gain rate of the battery from the ambient air
    Assumptions:
    Earth Atmospheric composition
    
    Inputs:
    power              [W]
    battery.
      mass_gain_factor [kg/W]
      
    Outputs:
      mdot             [kg/s]
    """
    
    #weight gain of battery (positive means mass loss)
    mdot = -(power) *(battery.mass_gain_factor)  
                
    return mdot


def find_mass_gain_rate(State, Settings, System):
	#TODO: battery = [Replace With State, Settings, or System Attribute]
	#TODO: power   = [Replace With State, Settings, or System Attribute]

	results = func_find_mass_gain_rate('battery', 'power')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System