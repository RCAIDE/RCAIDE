## @ingroup Methods-Flight_Dynamics-Dynamic_Stability-Full_Linearized_Equations-Supporting_Functions
# cz_u.py
# 
# Created:  Jun 2014, A. Wendorff
# Modified: Jan 2016, E. Botero

# ----------------------------------------------------------------------
#   Method
# ----------------------------------------------------------------------

## @ingroup Methods-Flight_Dynamics-Dynamic_Stability-Full_Linearized_Equations-Supporting_Functions
def func_cz_u(cL, U, cL_u = 0):
    """ This calculates the coefficient of force in the z direction
    with respect to the change in the forward velocity        

    Assumptions:
    None

    Source:
    J.H. Blakelock, "Automatic Control of Aircraft and Missiles" 
    Wiley & Sons, Inc. New York, 1991, (pg 23)

    Inputs:
    cL                 [dimensionless]
    U                  [meters/second]
    cL_u               

    Outputs:
    cz_u               [dimensionless]

    Properties Used:
    N/A           
    """

    # Generating Stability derivative
    
    cz_u = -2. * cL - U * cL_u
    
    return cz_u


cz_u(State, Settings, System):
	#TODO: cL   = [Replace With State, Settings, or System Attribute]
	#TODO: U    = [Replace With State, Settings, or System Attribute]
	#TODO: cL_u = [Replace With State, Settings, or System Attribute]

	results = func_cz_u('cL', 'U', 'cL_u')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System