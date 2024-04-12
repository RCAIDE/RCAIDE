## @ingroup Methods-Flight_Dynamics-Dynamic_Stability-Full_Linearized_Equations-Supporting_Functions
# cn_r.py
# 
# Created:  Jun 2014, A. Wendorff
# Modified: Jan 2016, E. Botero

# ----------------------------------------------------------------------
#   Method
# ----------------------------------------------------------------------

## @ingroup Methods-Flight_Dynamics-Dynamic_Stability-Full_Linearized_Equations-Supporting_Functions
def func_cn_r(cDw, Sv, Sref, l_v, span, eta_v, cLv_alpha):
    """ This calculats the yawing moment coefficient with respect to 
    perturbational angular rate around the z-body-axis           

    Assumptions:
    None
    
    Source:
    J.H. Blakelock, "Automatic Control of Aircraft and Missiles" 
    Wiley & Sons, Inc. New York, 1991, (pg 23)
    
    Inputs:
    eta_v              [dimensionless]
    cDw                [dimensionless]
    l_v                [meters]
    span               [meters]
    Sref               [meters**2]
    Sv                 [meters**2]
             
    Outputs:
    cn_r               [dimensionless]
            
    Properties Used:
    N/A           
    """

    # Generating Stability derivative
    cn_r = -cDw/4. - 2. * Sv / Sref * (l_v/span)**2. * cLv_alpha * eta_v
    
    return cn_r


cn_r(State, Settings, System):
	#TODO: cDw       = [Replace With State, Settings, or System Attribute]
	#TODO: Sv        = [Replace With State, Settings, or System Attribute]
	#TODO: Sref      = [Replace With State, Settings, or System Attribute]
	#TODO: l_v       = [Replace With State, Settings, or System Attribute]
	#TODO: span      = [Replace With State, Settings, or System Attribute]
	#TODO: eta_v     = [Replace With State, Settings, or System Attribute]
	#TODO: cLv_alpha = [Replace With State, Settings, or System Attribute]

	results = func_cn_r('cDw', 'Sv', 'Sref', 'l_v', 'span', 'eta_v', 'cLv_alpha')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System