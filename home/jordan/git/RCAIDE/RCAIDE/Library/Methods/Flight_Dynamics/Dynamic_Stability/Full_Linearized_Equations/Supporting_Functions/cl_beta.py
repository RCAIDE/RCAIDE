## @ingroup Methods-Flight_Dynamics-Dynamic_Stability-Full_Linearized_Equations-Supporting_Functions
# cl_beta.py
#
# Created:  Aug 2016, A. van Korlaar
# Modified: Aug 2016, L. Kulik

# ----------------------------------------------------------------------
#   Method
# ----------------------------------------------------------------------

## @ingroup Methods-Flight_Dynamics-Dynamic_Stability-Full_Linearized_Equations-Supporting_Functions
def func_cl_beta (geometry, cl_p):
    """THis calculates the derivative of roll rate with respect 
    to sideslip (dihedral effect)
    Assumptions: 
    None: 
    
    Source:
    STABILITY, USAF. "Control Datcom." Air Force Flight Dynamics Laboratory, 
    Wright-Patterson Air Force Base, Ohio (1972) 
    
    Inputs:
    dihedral    [radians]
    taper       [dimensionless]

    Outputs:
    cl_beta     [dimensionless]
    
    Properties Used:
    N/A
    """  

    taper = geometry.wings['main_wing'].taper
    dihedral = geometry.wings['main_wing'].dihedral

    # Generating Stability derivative
    cl_beta = dihedral*((1.+2.*taper)/(1.+3.*taper))*cl_p

    return cl_beta


def cl_beta(State, Settings, System):
	#TODO: geometry = [Replace With State, Settings, or System Attribute]
	#TODO: cl_p     = [Replace With State, Settings, or System Attribute]

	results = func_cl_beta('geometry', 'cl_p')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System