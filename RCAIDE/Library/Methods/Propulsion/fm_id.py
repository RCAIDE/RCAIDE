## @ingroup Methods-Propulsion
# fm_id.py
#
# Created:  ### ####, SUAVE Team
# Modified: Feb 2016, E. Botero
#           Dec 2017, W. Maier

# ----------------------------------------------------------------------
#  fm_id
# ----------------------------------------------------------------------

## @ingroup Methods-Propulsion

def func_fm_id(M,gamma):
    """Function that takes in the Mach number and isentropic expansion factor,
    and outputs a value for f(M) that's commonly used in compressible flow
    calculations.

    Inputs:
    M       [-]
    gamma   [-]

    Outputs:
    fm      [-]

    Spurce:
    https://web.stanford.edu/~cantwell/AA210A_Course_Material/AA210A_Course_Notes/
    """

    m0 = (gamma+1.)/(2.*(gamma-1.))
    m1 = ((gamma+1.)/2.)**m0
    m2 = (1.+(gamma-1.)/2.*M*M)**m0
    fm = m1*M/m2

    return fm



def fm_id(State, Settings, System):
	#TODO: M     = [Replace With State, Settings, or System Attribute]
	#TODO: gamma = [Replace With State, Settings, or System Attribute]

	results = func_fm_id('M', 'gamma')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System