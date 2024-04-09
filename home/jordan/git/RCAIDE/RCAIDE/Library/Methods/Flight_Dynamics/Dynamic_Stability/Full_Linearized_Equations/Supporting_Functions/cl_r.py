## @ingroup Methods-Flight_Dynamics-Dynamic_Stability-Full_Linearized_Equations-Supporting_Functions
# cl_r.py
# 
# Created:  Jun 2014, A. Wendorff
# Modified: Jan 2016, E. Botero

# ----------------------------------------------------------------------
#   Method
# ----------------------------------------------------------------------
## @ingroup Methods-Flight_Dynamics-Dynamic_Stability-Full_Linearized_Equations-Supporting_Functions
def func_cl_r(cLw):
    """ This calculates the rolling moment coefficient with respect to
    perturbational angular rate around the z-body-axis        
    
    Assumptions:
    None
    
    Source:
    J.H. Blakelock, "Automatic Control of Aircraft and Missiles" 
    Wiley & Sons, Inc. New York, 1991, (pg 23
    
    Inputs:
    clw          [dimensionless]
             
    Outputs:
    cl_r         [dimensionless]
            
    Properties Used:
    N/A                
    """

    # Generating Stability derivative
    cl_r = cLw/4.
    
    return cl_r


def cl_r(State, Settings, System):
	#TODO: cLw = [Replace With State, Settings, or System Attribute]

	results = func_cl_r('cLw',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System