## @ingroup Methods-Flight_Dynamics-Dynamic_Stability-Full_Linearized_Equations-Supporting_Functions
# cz_alphadot.py
# 
# Created:  Jun 2014, A. Wendorff
# Modified: Jan 2016, E. Botero

# ----------------------------------------------------------------------
#   Method
# ----------------------------------------------------------------------

## @ingroup Methods-Flight_Dynamics-Dynamic_Stability-Full_Linearized_Equations-Supporting_Functions
def func_cz_alphadot(cm_i, ep_alpha):
    """This calculates the coefficient of force in the z direction with 
    respect to the rate of change of the alpha of attack of the aircraft        

    Assumptions:
    None

    Source:
    J.H. Blakelock, "Automatic Control of Aircraft and Missiles" 
    Wiley & Sons, Inc. New York, 1991, (pg 23)

    Inputs:
    cm_i                       [dimensionless]
    ep_alpha                   [dimensionless]

    Outputs:
    cz_alphadot                [dimensionless]

    Properties Used:
    N/A           
    """

    # Generating Stability derivative

    cz_alphadot  = 2. * cm_i * ep_alpha
    
    return cz_alphadot 


cz_alphadot(State, Settings, System):
	#TODO: cm_i     = [Replace With State, Settings, or System Attribute]
	#TODO: ep_alpha = [Replace With State, Settings, or System Attribute]

	results = func_cz_alphadot('cm_i', 'ep_alpha')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System