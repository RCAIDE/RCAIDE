## @ingroup Methods-Cryogenic-Dynamo
# dynamo_efficiency.py
#
# Created:  Feb 2022,  S. Claridge

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# suave imports
import Legacy.trunk.S as SUAVE
import numpy as np
from Legacy.trunk.S.Components.Energy.Energy_Component import Energy_Component

# ----------------------------------------------------------------------
#  Estimated efficiency of HTS Dynamo 
# ----------------------------------------------------------------------
## @ingroup Methods-Cryogenic-Dynamos
def func_efficiency_curve(Dynamo, current):

    """ This sets the default values.

    Assumptions:
        The efficiency curve of the Dynamo is a parabola 

    Source:
        "Practical Estimation of HTS Dynamo Losses" - Kent Hamilton, Member, IEEE, Ratu Mataira-Cole, Jianzhao Geng, Chris Bumby, Dale Carnegie, and Rod Badcock, Senior Member, IEEE

    Inputs:
        current        [A]

    Outputs:
        efficiency      [W/W]

    Properties Used:
        None
    """     

    x = np.array(current)

    if np.any(x > Dynamo.rated_current * 1.8 ) or np.any(x < Dynamo.rated_current * 0.2): #Plus minus 80
        print("Current out of range")
        return 0 

    a          = ( Dynamo.efficiency ) / np.square(Dynamo.rated_current) #one point on the graph is assumed to be  (0, 2 * current), 0  = a (current ^ 2) + efficiency 
    
    efficiency = -a * (np.square( x - Dynamo.rated_current) ) +  Dynamo.efficiency # y = -a(x - current)^2 + efficieny 

    return   efficiency


efficiency_curve(State, Settings, System):
	#TODO: Dynamo  = [Replace With State, Settings, or System Attribute]
	#TODO: current = [Replace With State, Settings, or System Attribute]

	results = func_efficiency_curve('Dynamo', 'current')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System