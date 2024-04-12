## @ingroup Methods-Costs-Operating_Costs
# compute_operating_costs.py
#
# Created:  

# suave imports
from Legacy.trunk.S.Core import Units,Data

# ----------------------------------------------------------------------
#  Compute operating costs
# ----------------------------------------------------------------------

## @ingroup Methods-Costs-Operating_Costs
def func_compute_operating_costs(vehicle):
    """ This is a stub. It is called by the default costs analysis, but does nothing."""
    pass

    return



compute_operating_costs(State, Settings, System):
	#TODO: vehicle = [Replace With State, Settings, or System Attribute]

	results = func_compute_operating_costs('vehicle',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System