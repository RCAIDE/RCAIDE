## @ingroup Library-Methods-Noise-Correlation_Buildup-Engine 
# RCAIDE/Library/Methods/Noise/Correlation_Buildup/Engine/angle_of_attack_effect.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
# Python package imports   
import numpy as np   

# ----------------------------------------------------------------------------------------------------------------------     
#  Angle of Attack Effect
# ----------------------------------------------------------------------------------------------------------------------     
## @ingroup Library-Methods-Noise-Correlation_Buildup-Engine
def angle_of_attack_effect(AoA,Mach_aircraft,theta_m):
    """This calculates the angle of attack effect, in decibels, to be added 
    to the predicted mixed jet noise level. 
        
    Assumptions:
        N/A

    Source:
        SAE Model
    
    Inputs:   
        AoA           angle of attack         [rad]
        Mach_aircraft mach number of aircraft [Unitless]
        theta_m       emission angle          [rad]                
    
    Outputs:
        ATK_m         angle of attack effect  [Unitless]    
    
    Properties Used:
        None 
    """

    # Angle of attack effect
    ATK_m = 0.5*AoA*Mach_aircraft*((1.8*theta_m/np.pi)-0.6)**2

    return ATK_m



def _angle_of_attack_effect(State, Settings, System):
	'''
	Framework version of angle_of_attack_effect.
	Wraps angle_of_attack_effect with State, Settings, System pack/unpack.
	Please see angle_of_attack_effect documentation for more details.
	'''

	#TODO: AoA           = [Replace With State, Settings, or System Attribute]
	#TODO: Mach_aircraft = [Replace With State, Settings, or System Attribute]
	#TODO: theta_m       = [Replace With State, Settings, or System Attribute]

	results = angle_of_attack_effect('AoA', 'Mach_aircraft', 'theta_m')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System