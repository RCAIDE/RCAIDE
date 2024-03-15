## @ingroup Library-Methods-Energy-Battery-Common
# RCAIDE/Library/Methods/Energy/Sources/Battery/Common/initialize_from_mass.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Energy-Battery-Common
def initialize_from_mass(battery,module_weight_factor = 1.42 ):
    """
    Calculate the max energy and power based of the mass
    Assumptions:
    A constant value of specific energy and power

    Inputs:
    mass              [kilograms]
    battery.
      specific_energy [J/kg]               
      specific_power  [W/kg]

    Outputs:
     battery.
       maximum_energy
       maximum_power
       mass_properties.
        mass


    """     
    mass = battery.mass_properties.mass/module_weight_factor
    
    if battery.cell.mass == None: 
        n_series   = 1
        n_parallel = 1 
    else:
        n_cells    = int(mass/battery.cell.mass)
        n_series   = int(battery.pack.maximum_voltage/battery.cell.maximum_voltage)
        n_parallel = int(n_cells/n_series)
        
    battery.pack.maximum_energy                    = mass*battery.specific_energy  
    battery.pack.maximum_power                     = mass*battery.specific_power
    battery.pack.initial_maximum_energy            = battery.pack.maximum_energy    
    battery.pack.electrical_configuration.series   = n_series
    battery.pack.electrical_configuration.parallel = n_parallel 
    battery.pack.electrical_configuration.total    = n_parallel*n_series      
    battery.charging_voltage                       = battery.cell.charging_voltage * battery.pack.electrical_configuration.series     
    battery.charging_current                       = battery.cell.charging_current * battery.pack.electrical_configuration.parallel        


def _initialize_from_mass(State, Settings, System):
	'''
	Framework version of initialize_from_mass.
	Wraps initialize_from_mass with State, Settings, System pack/unpack.
	Please see initialize_from_mass documentation for more details.
	'''

	#TODO: battery              = [Replace With State, Settings, or System Attribute]
	#TODO: module_weight_factor = [Replace With State, Settings, or System Attribute]

	results = initialize_from_mass('battery', 'module_weight_factor')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System