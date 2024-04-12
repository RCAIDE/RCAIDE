## @ingroup Methods-Power-Fuel_Cell-Discharge
# zero_fidelity.py
#
# Created : Apr 2015, M. Vegh 
# Modified: Sep 2015, M. Vegh
#           Feb 2016, E. Botero

# ----------------------------------------------------------------------
#  Zero Fidelity
# ----------------------------------------------------------------------

## @ingroup Methods-Power-Fuel_Cell-Discharge
def func_zero_fidelity(fuel_cell,conditions,numerics):
    '''
    Assumptions:
    constant efficiency
    
    Inputs:
        fuel_cell.
            inputs.
                power_in              [W]
            propellant.
                specific_energy       [J/kg]
            efficiency    
    
    Outputs:
        mdot                          [kg/s]
    
    '''
    
    
    power       = fuel_cell.inputs.power_in
    
    #mass flow rate of the fuel  
    mdot        = power/(fuel_cell.propellant.specific_energy*fuel_cell.efficiency)                      
  
    return mdot


def zero_fidelity(State, Settings, System):
	#TODO: fuel_cell  = [Replace With State, Settings, or System Attribute]
	#TODO: conditions = [Replace With State, Settings, or System Attribute]
	#TODO: numerics   = [Replace With State, Settings, or System Attribute]

	results = func_zero_fidelity('fuel_cell', 'conditions', 'numerics')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System