## @ingroup Library-Methods-Energy-Battery-Common
# RCAIDE/Library/Methods/Energy/Sources/Battery/Common/find_total_mass_gain.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Energy-Battery-Common
def find_total_mass_gain(battery):
    """finds the total mass of air that the battery 
    accumulates when discharged fully
    
    Assumptions:
    Earth Atmospheric composition
    
    Inputs:
    battery.pack.maximum_energy [J]
    battery.
      mass_gain_factor [kg/W]
      
    Outputs:
      mdot             [kg]
    """ 
    
    mgain=battery.pack.maximum_energy*battery.mass_gain_factor
    
    return mgain


def _find_total_mass_gain(State, Settings, System):
	'''
	Framework version of find_total_mass_gain.
	Wraps find_total_mass_gain with State, Settings, System pack/unpack.
	Please see find_total_mass_gain documentation for more details.
	'''

	#TODO: battery = [Replace With State, Settings, or System Attribute]

	results = find_total_mass_gain('battery',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System