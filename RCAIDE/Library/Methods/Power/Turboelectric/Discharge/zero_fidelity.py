## @ingroup Methods-Power-Turboelectric-Discharge
# zero_fidelity.py
#
# Created : Nov 2019,   K. Hamilton - Through New Zealand Ministry of Business Innovation and Employment Research Contract RTVU2004
# Modified: Nov 2021,   S. Claridge
# ----------------------------------------------------------------------
#  Zero Fidelity
#  ----------------------------------------------------------------------

## @ingroup Methods-Power-Turboelectric-Discharge
def func_zero_fidelity(turboelectric,conditions,numerics):
    '''
    Assumptions:
    constant efficiency
    
    Inputs:
        turboelectric.
            inputs.
                power_in              [W]
            propellant.
                specific_energy       [J/kg]
            efficiency    
    
    Outputs:
        mdot                          [kg/s]
    
    '''
    
    
    power       = turboelectric.inputs.power_in
    
    #mass flow rate of the fuel  
    mdot        = power/(turboelectric.propellant.specific_energy*turboelectric.efficiency)          
  
    return mdot



zero_fidelity(State, Settings, System):
	#TODO: turboelectric = [Replace With State, Settings, or System Attribute]
	#TODO: conditions    = [Replace With State, Settings, or System Attribute]
	#TODO: numerics      = [Replace With State, Settings, or System Attribute]

	results = func_zero_fidelity('turboelectric', 'conditions', 'numerics')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System