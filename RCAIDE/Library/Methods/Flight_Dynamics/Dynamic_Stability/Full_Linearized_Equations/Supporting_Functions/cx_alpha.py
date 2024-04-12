## @ingroup Methods-Flight_Dynamics-Dynamic_Stability-Full_Linearized_Equations-Supporting_Functions
# cx_alpha.py
# 
# Created:  Jun 2014, A. Wendorff
# Modified: Jan 2016, E. Botero

# ----------------------------------------------------------------------
#   Method
# ----------------------------------------------------------------------

## @ingroup Methods-Flight_Dynamics-Dynamic_Stability-Full_Linearized_Equations-Supporting_Functions
def func_cx_alpha(cL, cL_alpha):
    """ This calculates the coefficient of force in the x direction
    with respect to the change in angle of attack of the aircraft        
    
    Assumptions:
    None
    
    Source:
    J.H. Blakelock, "Automatic Control of Aircraft and Missiles" 
    Wiley & Sons, Inc. New York, 1991, (pg 23)
    
    Inputs:
    cL              [dimensionless]
    cL_alpha        [dimensionless]
             
    Outputs:
    cx_alpha        [dimensionless]
            
    Properties Used:
    N/A                
    """

    # Generating Stability derivative
    cx_alpha  = cL - cL_alpha
    
    return cx_alpha


cx_alpha(State, Settings, System):
	#TODO: cL       = [Replace With State, Settings, or System Attribute]
	#TODO: cL_alpha = [Replace With State, Settings, or System Attribute]

	results = func_cx_alpha('cL', 'cL_alpha')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System