## @ingroup Methods-Aerodynamics-Common-Fidelity_Zero-Lift
# aircraft_total.py
# 
# Created:  Dec 2013, A. Variyar,
# Modified: Feb 2014, A. Variyar, T. Lukaczyk, T. Orra 
#           Apr 2014, A. Variyar   
#           Jan 2016, E. Botero       


# ----------------------------------------------------------------------
#  Aircraft Total
# ----------------------------------------------------------------------
## @ingroup Methods-Aerodynamics-Common-Fidelity_Zero-Lift 
def func_aircraft_total(state,settings,geometry):
    """Returns total aircraft lift and stores values

    Assumptions:
    None

    Source:
    None

    Inputs:
    state.conditions.aerodynamics.lift_coefficient    [Unitless]

    Outputs:
    aircraft_lift_total (lift coefficient)            [Unitless]

    Properties Used:
    N/A
    """      
    
    aircraft_lift_total = state.conditions.aerodynamics.lift_coefficient

    return aircraft_lift_total



def aircraft_total(State, Settings, System):
	#TODO: state    = [Replace With State, Settings, or System Attribute]
	#TODO: settings = [Replace With State, Settings, or System Attribute]
	#TODO: geometry = [Replace With State, Settings, or System Attribute]

	results = func_aircraft_total('state', 'settings', 'geometry')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System