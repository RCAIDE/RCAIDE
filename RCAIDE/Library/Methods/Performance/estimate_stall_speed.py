## @ingroup Library-Methods-Performance
# RCAIDE/Library/Methods/Performance/estimate_stall_speed.py
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

#------------------------------------------------------------------------------
# Stall Speed Estimation
#------------------------------------------------------------------------------

## @ingroup Library-Methods-Performance
def estimate_stall_speed(vehicle_mass,reference_area,altitude,maximum_lift_coefficient):

    """Calculates the stall speed of an aircraft at a given altitude and a maximum lift coefficient.

        Sources:
        N/A

        Assumptions:
        None 

        Inputs:
            vehicle_mass                    vehicle mass             [kg]
            reference_area                  vehicle reference area   [m^2] 
            altitude                        cruise altitude          [m]
            maximum_lift_coefficient        maximum lift coefficient [unitless] 
            
        Outputs: 
            V_stall                         stall speed              [m/s]
    """ 
      
    g       = 9.81 
    atmo    = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    rho     = atmo.compute_values(altitude,0.).density 
    V_stall = float(np.sqrt(2.*vehicle_mass*g/(rho*reference_area*maximum_lift_coefficient)))  
    
    return V_stall


def _estimate_stall_speed(State, Settings, System):
	'''
	Framework version of estimate_stall_speed.
	Wraps estimate_stall_speed with State, Settings, System pack/unpack.
	Please see estimate_stall_speed documentation for more details.
	'''

	#TODO: vehicle_mass             = [Replace With State, Settings, or System Attribute]
	#TODO: reference_area           = [Replace With State, Settings, or System Attribute]
	#TODO: altitude                 = [Replace With State, Settings, or System Attribute]
	#TODO: maximum_lift_coefficient = [Replace With State, Settings, or System Attribute]

	results = estimate_stall_speed('vehicle_mass', 'reference_area', 'altitude', 'maximum_lift_coefficient')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System