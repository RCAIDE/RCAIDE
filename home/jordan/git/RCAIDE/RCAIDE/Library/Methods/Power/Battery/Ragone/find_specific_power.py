## @ingroup Methods-Power-Battery-Ragone
# find_specific_power.py
# 
# Created:  ### 2104, M. Vegh
# Modified: Sep 2105, M. Vegh
#           Feb 2016, E. Botero

# ----------------------------------------------------------------------
#  Find Specific Power
# ----------------------------------------------------------------------

## @ingroup Methods-Power-Battery-Ragone
def func_find_specific_power(battery, specific_energy):
    """determines specific specific power from a ragone curve correlation
    Assumptions:
    None
    
    Inputs:
    battery.
      specific_energy [J/kg]               
      ragone.
        constant_1    [W/kg]
        constant_2    [J/kg]
                
    Outputs:
    battery.
      specific_power  [W/kg]   
    
    
    
    """
    
    const_1                 = battery.ragone.const_1
    const_2                 = battery.ragone.const_2
    specific_power          = const_1*10.**(const_2*specific_energy)
    battery.specific_power  = specific_power
    battery.specific_energy = specific_energy


def find_specific_power(State, Settings, System):
	#TODO: battery         = [Replace With State, Settings, or System Attribute]
	#TODO: specific_energy = [Replace With State, Settings, or System Attribute]

	results = func_find_specific_power('battery', 'specific_energy')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System