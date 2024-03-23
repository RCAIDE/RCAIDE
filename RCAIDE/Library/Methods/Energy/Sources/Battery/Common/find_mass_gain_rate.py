## @ingroup Library-Methods-Energy-Battery-Common
# RCAIDE/Library/Methods/Energy/Sources/Battery/Common/find_mass_gain_rate.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Energy-Battery-Common
def find_mass_gain_rate(battery,power):
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


def _find_mass_gain_rate(State, Settings, System):
	'''
	Framework version of find_mass_gain_rate.
	Wraps find_mass_gain_rate with State, Settings, System pack/unpack.
	Please see find_mass_gain_rate documentation for more details.
	'''

	#TODO: battery = [Replace With State, Settings, or System Attribute]
	#TODO: power   = [Replace With State, Settings, or System Attribute]

	results = find_mass_gain_rate('battery', 'power')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System