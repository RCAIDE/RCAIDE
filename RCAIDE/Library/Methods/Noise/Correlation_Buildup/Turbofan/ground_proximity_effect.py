## @ingroup Library-Methods-Noise-Correlation_Buildup-Engine
# RCAIDE/Library/Methods/Noise/Correlation_Buildup/Engine/external_plug_effect.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
 
# Python package imports   
import numpy as np   

# ----------------------------------------------------------------------------------------------------------------------     
#  Ground Proximity Effect
# ----------------------------------------------------------------------------------------------------------------------     
## @ingroup Library-Methods-Noise-Correlation_Buildup-Engine    
def ground_proximity_effect (Velocity_mixed,sound_ambient,theta_m,engine_height,Diameter_mixed,frequency):
    """This function calculates the ground proximity effect, in decibels, and is used for full-scale 
    engine test stand.
        
    Assumptions:
        N/A

    Source:
        N/A

    Inputs:
        Velocity_mixed  [m/s]
        sound_ambient   [SPL]
        theta_m         [rad]
        engine_height   [m]
        Diameter_mixed  [m]
        frequency       [1/s]

    Outputs:
        GPROX_m         [dB]

    Properties Used:
        N/A 
    """ 
    # Ground proximity is applied only for the mixed jet component
    GPROX_m = (5*Velocity_mixed/sound_ambient)*np.exp(-(9*(theta_m/np.pi)-6.75)**2- \
        ((engine_height/Diameter_mixed)-2.5)**2)*(1+(np.sin((np.pi*engine_height*frequency/sound_ambient)-np.pi/2))**2)/ \
        (2+np.abs((engine_height*frequency/sound_ambient)-1))

    return GPROX_m


def _ground_proximity_effect(State, Settings, System):
	'''
	Framework version of ground_proximity_effect.
	Wraps ground_proximity_effect with State, Settings, System pack/unpack.
	Please see ground_proximity_effect documentation for more details.
	'''

	#TODO: Velocity_mixed = [Replace With State, Settings, or System Attribute]
	#TODO: sound_ambient  = [Replace With State, Settings, or System Attribute]
	#TODO: theta_m        = [Replace With State, Settings, or System Attribute]
	#TODO: engine_height  = [Replace With State, Settings, or System Attribute]
	#TODO: Diameter_mixed = [Replace With State, Settings, or System Attribute]
	#TODO: frequency      = [Replace With State, Settings, or System Attribute]

	results = ground_proximity_effect('Velocity_mixed', 'sound_ambient', 'theta_m', 'engine_height', 'Diameter_mixed', 'frequency')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System