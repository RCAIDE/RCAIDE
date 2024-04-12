## @ingroup Methods-Geometry-Two_Dimensional-Cross_Section-Planform
# vertical_tail_planform.py
#
# Created:  Mar 2013, SUAVE Team
# Modified: Jan 2016, E. Botero

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from .wing_planform import wing_planform

# ----------------------------------------------------------------------
#  Methods
# ----------------------------------------------------------------------
## @ingroup Methods-Geometry-Two_Dimensional-Cross_Section-Planform
def func_vertical_tail_planform(Wing):
    """Calls generic wing planform function to compute wing planform values

    Assumptions:
    None

    Source:
    None

    Inputs:
    Wing             [SUAVE data structure]

    Outputs:
    Changes to Wing (see wing_planform)

    Properties Used:
    N/A
    """  
    wing_planform(Wing)
    return 0
    


def vertical_tail_planform(State, Settings, System):
	#TODO: Wing = [Replace With State, Settings, or System Attribute]

	results = func_vertical_tail_planform('Wing',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System