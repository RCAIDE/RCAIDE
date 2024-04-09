## @ingroup Methods-Aerodynamics-Common-Fidelity_Zero-Drag
# spoiler_drag.py
#
# Created:  Jan 2014, A. Variyar
# Modified: Jan 2016, E. Botero 

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
#  Adds the spoiler drag
# ----------------------------------------------------------------------

## @ingroup Methods-Aerodynamics-Common-Fidelity_Zero-Drag
def func_spoiler_drag(state,settings,geometry):
    """Adds a spoiler drag increment

    Assumptions:
    None

    Source:
    None

    Inputs:
    settings.spoiler_drag_increment  [Unitless]

    Outputs:
    spoiler_drag                     [Unitless]

    Properties Used:
    N/A
    """    
    
    # unpack inputs
    conditions     = state.conditions
    configuration  = settings
    drag_breakdown = conditions.aerodynamics.drag_breakdown

    # various drag components
    spoiler_drag = settings.spoiler_drag_increment

    # untrimmed drag
    conditions.aerodynamics.drag_breakdown.spoiler_drag = spoiler_drag
    
    return spoiler_drag



def spoiler_drag(State, Settings, System):
	#TODO: state    = [Replace With State, Settings, or System Attribute]
	#TODO: settings = [Replace With State, Settings, or System Attribute]
	#TODO: geometry = [Replace With State, Settings, or System Attribute]

	results = func_spoiler_drag('state', 'settings', 'geometry')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System