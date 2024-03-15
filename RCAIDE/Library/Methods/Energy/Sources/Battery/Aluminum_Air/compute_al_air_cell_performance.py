## @ingroup Library-Methods-Energy-Battery-Aluminum_Air
# RCAIDE/Library/Methods/Energy/Sources/Battery/Aluminum_Air/compute_al_air_cell_performance.py
# 
# 
# Created:  Jul 2023, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  compute_al_air_cell_performance
# ---------------------------------------------------------------------------------------------------------------------- 

## @ingroup Library-Methods-Energy-Battery-Aluminum_Air
def find_aluminum_mass(battery, energy):
    aluminum_mass = energy*battery.aluminum_mass_factor
    return aluminum_mass 

def find_water_mass(battery, energy):
    water_mass = energy*battery.water_mass_gain_factor
    return water_mass



def _find_aluminum_mass(State, Settings, System):
	'''
	Framework version of find_aluminum_mass.
	Wraps find_aluminum_mass with State, Settings, System pack/unpack.
	Please see find_aluminum_mass documentation for more details.
	'''

	#TODO: battery = [Replace With State, Settings, or System Attribute]
	#TODO: energy  = [Replace With State, Settings, or System Attribute]

	results = find_aluminum_mass('battery', 'energy')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System


def _find_water_mass(State, Settings, System):
	'''
	Framework version of find_water_mass.
	Wraps find_water_mass with State, Settings, System pack/unpack.
	Please see find_water_mass documentation for more details.
	'''

	#TODO: battery = [Replace With State, Settings, or System Attribute]
	#TODO: energy  = [Replace With State, Settings, or System Attribute]

	results = find_water_mass('battery', 'energy')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System