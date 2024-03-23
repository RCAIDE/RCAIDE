## @ingroup Library-Methods-Aerodynamics-Common-Lift
# RCAIDE/Library/Methods/Aerodynamics/Common/Lift/aircraft_total.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Mar 2024 M. Carke     


# ----------------------------------------------------------------------
#  Aircraft Total
# ----------------------------------------------------------------------
## @ingroup Library-Methods-Aerodynamics-Common-Fidelity_Zero-Lift 
def aircraft_total(state,settings,geometry):
    """Returns the total aircraft lift of the aircraft 

    Assumptions:
    None

    Source:
    None

    Inputs:
    state.conditions.aerodynamics.coefficients.lift    [Unitless]

    Outputs:
    aircraft_lift_total (lift coefficient)            [Unitless]

    Properties Used:
    N/A
    """      
    
    aircraft_lift_total = state.conditions.aerodynamics.coefficients.lift

    return aircraft_lift_total



def _aircraft_total(State, Settings, System):
	'''
	Framework version of aircraft_total.
	Wraps aircraft_total with State, Settings, System pack/unpack.
	Please see aircraft_total documentation for more details.
	'''

	#TODO: state    = [Replace With State, Settings, or System Attribute]
	#TODO: settings = [Replace With State, Settings, or System Attribute]
	#TODO: geometry = [Replace With State, Settings, or System Attribute]

	results = aircraft_total('state', 'settings', 'geometry')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System