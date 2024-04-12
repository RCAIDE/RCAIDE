## @ingroup Methods-Power-Fuel_Cell-Sizing

# initialize_from_power.py
#
# Created : Apr 2015, M. Vegh 
# Modified: Feb 2016, E. Botero
           
# ----------------------------------------------------------------------
#  Initialize from Power
# ----------------------------------------------------------------------

## @ingroup Methods-Power-Fuel_Cell-Sizing
def func_initialize_from_power(fuel_cell,power):
    '''
    assigns the mass of the fuel cell based on the power and specific power
    Assumptions:
    None
    
    Inputs:
    power            [J]
    fuel_cell.
      specific_power [W/kg]
    
    
    Outputs:
    fuel_cell.
      mass_properties.
        mass         [kg]
    '''
    fuel_cell.mass_properties.mass=power/fuel_cell.specific_power



initialize_from_power(State, Settings, System):
	#TODO: fuel_cell = [Replace With State, Settings, or System Attribute]
	#TODO: power     = [Replace With State, Settings, or System Attribute]

	results = func_initialize_from_power('fuel_cell', 'power')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System