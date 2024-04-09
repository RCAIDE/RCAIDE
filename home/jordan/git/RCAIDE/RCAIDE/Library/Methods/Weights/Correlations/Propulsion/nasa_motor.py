## @ingroup Methods-Weights-Correlations-Propulsion
# air_cooled_motor.py
# 
# Created:  Jan 2014, M. Vegh, 
# Modified: Jan 2014, A. Wendorff
#           Feb 2016, E. Botero
#           Mar 2020, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

from Legacy.trunk.S.Core import Units

# ----------------------------------------------------------------------
#   Air Cooled Motor
# ----------------------------------------------------------------------

## @ingroup Methods-Weights-Correlations-Propulsion
def func_nasa_motor(torque, kwt2=.3928, xwt=.8587):
    """ Calculate the weight of an air-cooled motor    
    weight correlation; weight=kwt2*(max_power**xwt)
        
    Assumptions:
            calculated from fit of high power-to-weight motors
            
    Source: NDARC Theory Manual, Page 213
    https://ntrs.nasa.gov/archive/nasa/casi.ntrs.nasa.gov/20170011656.pdf
    
    Inputs:
            torque- maximum torque the motor can deliver safely      [N-m]
            kwt2
            xwt
            
    Outputs:
            mass- mass of the motor                                [kilograms]
        
    Properties Used:
            N/A
    """   
    trq  = torque/(Units.ft*Units.lbf)
    mass = kwt2*(trq**xwt) * Units.pounds # mass in kg
     
    return mass 


def nasa_motor(State, Settings, System):
	#TODO: torque = [Replace With State, Settings, or System Attribute]
	#TODO: kwt2   = [Replace With State, Settings, or System Attribute]
	#TODO: xwt    = [Replace With State, Settings, or System Attribute]

	results = func_nasa_motor('torque', 'kwt2', 'xwt')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System