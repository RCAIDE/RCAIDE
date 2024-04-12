## @ingroup Methods-Flight_Dynamics-Dynamic_Stability-Full_Linearized_Equations-Supporting_Functions
# cy_phi.py
# 
# Created:  Jun 2014, A. Wendorff
# Modified: Jan 2016, E. Botero

# ----------------------------------------------------------------------
#   Method
# ----------------------------------------------------------------------

## @ingroup Methods-Flight_Dynamics-Dynamic_Stability-Full_Linearized_Equations-Supporting_Functions
def func_cy_phi(CL):
    """ This calculates the force coefficient in the y direction 
    with respect to the roll angle of the aircraft        

    Assumptions:
    None

    Source:
    J.H. Blakelock, "Automatic Control of Aircraft and Missiles" 
    Wiley & Sons, Inc. New York, 1991, (pg 23)

    Inputs:
    CL                [dimensionless]

    Outputs:
    cy_phi            [dimensionless]

    Properties Used:
    N/A           
    """

    # Generating Stability derivative
    
    cy_phi = CL
    
    return cy_phi


cy_phi(State, Settings, System):
	#TODO: CL = [Replace With State, Settings, or System Attribute]

	results = func_cy_phi('CL',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System