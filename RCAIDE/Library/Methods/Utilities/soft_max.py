## @ingroup Methods-Utilities
#soft_max.py
#Created:  Feb 2016, M. Vegh

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import numpy as np


# ----------------------------------------------------------------------
# soft_max Method
# ----------------------------------------------------------------------
## @ingroup Methods-Utilities
def func_soft_max(x1,x2):
    """Computes the soft maximum of two inputs.

    Assumptions:
    None

    Source:
    http://www.johndcook.com/blog/2010/01/20/how-to-compute-the-soft-maximum/

    Inputs:
    x1   [-]
    x2   [-]

    Outputs:             
    f    [-] The soft max

    Properties Used:
    N/A
    """    
    max=np.maximum(x1,x2)
    min=np.minimum(x1,x2)
    f=max+np.log(1+np.exp(min-max))
    
    return f


def soft_max(State, Settings, System):
	#TODO: x1 = [Replace With State, Settings, or System Attribute]
	#TODO: x2 = [Replace With State, Settings, or System Attribute]

	results = func_soft_max('x1', 'x2')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System