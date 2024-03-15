## @ingroup Library-Methods-Performance
# RCAIDE/Library/Methods/Performance/estimate_cruise_drag.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
import RCAIDE
 
# Pacakge imports 
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
# Cruise Drag Function
# ----------------------------------------------------------------------------------------------------------------------

## @ingroup Library-Methods-Performance
def estimate_cruise_drag(vehicle,altitude,speed,lift_coefficient = 0.5 ,profile_drag = 0.05):

    """Calculates the drag force of an aircraft at a given altitude and  cruising speed.

        Sources:
        N/A

        Assumptions:
        None 

        Inputs:
            vehicle                         vehicle    
            altitude                        cruise altitude          [m] 
            speed                           cruise speed             [m/s] 
            lift_coefficient                cruise lift coefficient  [-] 
            
        Outputs: 
            Drag                            cruise drag              [N]
    """ 
       
    atmo = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    rho  = atmo.compute_values(altitude,0.).density[0][0]  
    S    = vehicle.reference_area                     # reference area   
    AR   = vehicle.wings.main_wing.aspect_ratio       # aspect ratio  
    Cdi  = lift_coefficient**2/(np.pi*AR*0.98)        # induced drag
    Cd   = profile_drag + Cdi                         # total drag 
    Drag = S * (0.5*rho*speed**2 )*Cd                 # cruise drag 
    
    return Drag


def _estimate_cruise_drag(State, Settings, System):
	'''
	Framework version of estimate_cruise_drag.
	Wraps estimate_cruise_drag with State, Settings, System pack/unpack.
	Please see estimate_cruise_drag documentation for more details.
	'''

	#TODO: vehicle          = [Replace With State, Settings, or System Attribute]
	#TODO: altitude         = [Replace With State, Settings, or System Attribute]
	#TODO: speed            = [Replace With State, Settings, or System Attribute]
	#TODO: lift_coefficient = [Replace With State, Settings, or System Attribute]
	#TODO: profile_drag     = [Replace With State, Settings, or System Attribute]

	results = estimate_cruise_drag('vehicle', 'altitude', 'speed', 'lift_coefficient', 'profile_drag')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System