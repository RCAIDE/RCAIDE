# @ingroup Methods-Flight_Dynamics-Dynamic_Stability-Full_Linearized_Equations-Supporting_Functions
# cz_alpha.py
# 
# Created:  Jun 2014, A. Wendorff
# Modified: Jan 2016, E. Botero

# ----------------------------------------------------------------------
#   Method
# ----------------------------------------------------------------------

# @ingroup Methods-Flight_Dynamics-Dynamic_Stability-Full_Linearized_Equations-Supporting_Functions
def func_cz_alpha(cD, cL_alpha):
    """ This calculates the coefficient of force in the z-direction
    with respect to alpha of attack of the aircraft        

    Assumptions:
    None

    Source:
    J.H. Blakelock, "Automatic Control of Aircraft and Missiles" 
    Wiley & Sons, Inc. New York, 1991, (pg 23)

    Inputs:
    cD                         [dimensionless]
    cL_alpha                   [dimensionless]

    Outputs:
    cz_alpha                   [dimensionless]

    Properties Used:
    N/A           
    """

    # Generating Stability derivative

    cz_alpha  = -cD - cL_alpha
    
    return cz_alpha 


cz_alpha(State, Settings, System):
	#TODO: cD       = [Replace With State, Settings, or System Attribute]
	#TODO: cL_alpha = [Replace With State, Settings, or System Attribute]

	results = func_cz_alpha('cD', 'cL_alpha')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System