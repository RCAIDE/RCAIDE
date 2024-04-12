## @ingroup Methods-Flight_Dynamics-Dynamic_Stability-Full_Linearized_Equations-Supporting_Functions
# ep_alpha.py
# 
# Created:  Jun 2014, A. Wendorff
# Modified: Jan 2016, E. Botero

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import numpy as np

# ----------------------------------------------------------------------
#   Method
# ----------------------------------------------------------------------

## @ingroup Methods-Flight_Dynamics-Dynamic_Stability-Full_Linearized_Equations-Supporting_Functions
def func_ep_alpha(cL_w_alpha, Sref, span):
    """ Calculates the change in the downwash with change in 
    angle of attack         
    
    Assumptions:
    None
    
    Source:
    J.H. Blakelock, "Automatic Control of Aircraft and Missiles" 
    Wiley & Sons, Inc. New York, 1991, (pg 34)
    
    Inputs:
    span            [meters]
    Sref            [square meters]
    cL_w_alpha      [unitless]
             
    Outputs:
    ep_alpha        [Unitless]
            
    Properties Used:
    N/A                
    """

    # Generating Stability derivative
    ep_alpha = 2 * cL_w_alpha/ np.pi / (span ** 2. / Sref )
    
    return ep_alpha


def ep_alpha(State, Settings, System):
	#TODO: cL_w_alpha = [Replace With State, Settings, or System Attribute]
	#TODO: Sref       = [Replace With State, Settings, or System Attribute]
	#TODO: span       = [Replace With State, Settings, or System Attribute]

	results = func_ep_alpha('cL_w_alpha', 'Sref', 'span')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System