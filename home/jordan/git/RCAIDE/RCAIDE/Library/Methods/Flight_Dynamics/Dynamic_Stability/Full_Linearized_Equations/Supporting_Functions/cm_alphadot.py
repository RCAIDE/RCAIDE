## @ingroup Methods-Flight_Dynamics-Dynamic_Stability-Full_Linearized_Equations-Supporting_Functions
# cm_alphadot.py
# 
# Created:  Jun 2014, A. Wendorff
# Modified: Jan 2016, E. Botero

# ----------------------------------------------------------------------
#   Method
# ----------------------------------------------------------------------
## @ingroup Methods-Flight_Dynamics-Dynamic_Stability-Full_Linearized_Equations-Supporting_Functions
def func_cm_alphadot(cm_i, ep_alpha, l_t, mac):
    """ This calculates the pitching moment coefficient with respect to the 
    rate of change of the alpha of attack of the aircraft        

    Assumptions:
    None
    
    Source:
    J.H. Blakelock, "Automatic Control of Aircraft and Missiles" 
    Wiley & Sons, Inc. New York, 1991, (pg 23)
    
    Inputs:
    cm_i                [dimensionless]
    ep_alpha            [dimensionless]
    l_t                 [meters]
    mac                 [meters]
             
    Outputs:
    cm_alphadot         [dimensionless]
            
    Properties Used:
    N/A           
    """

    # Generating Stability derivative

    cm_alphadot  = 2. * cm_i * ep_alpha * l_t / mac
    
    return cm_alphadot 


def cm_alphadot(State, Settings, System):
	#TODO: cm_i     = [Replace With State, Settings, or System Attribute]
	#TODO: ep_alpha = [Replace With State, Settings, or System Attribute]
	#TODO: l_t      = [Replace With State, Settings, or System Attribute]
	#TODO: mac      = [Replace With State, Settings, or System Attribute]

	results = func_cm_alphadot('cm_i', 'ep_alpha', 'l_t', 'mac')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System