## @ingroup Methods-Noise-Fidelity_One-Noise_Tools
# decibel_arithmetic.py
# 
# Created: Apr 2021, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import numpy as np 
# -----------------------------------------------------------------------
# Decibel Arithmetic
# -----------------------------------------------------------------------
## @ingroup Methods-Noise-Fidelity_One-Noise_Tools
def func_pressure_ratio_to_SPL_arithmetic(p_pref_total):
    ''' This computes the total SPL given mutiple acoustic pressure ratios 
    of one of mutiple sources
    
    Assumptions:
        None

    Source:
        None

    Inputs:
        Pressure Ratios       [unitless]

    Outputs: 
        Sound Pressure Level  [decibel]

    Properties Used:
        N/A 
    
    '''
    SPL_total = 10*np.log10(np.sum(p_pref_total, axis = 3))
    return SPL_total

## @ingroup Methods-Noise-Fidelity_One-Noise_Tools
def func_SPL_arithmetic(SPL, sum_axis = 2):
    '''This computes the total SPL from multiple sources 
    using decibel arithmetic  
    
    Assumptions:
        None

    Source:
        None

    Inputs:
        SPL  -  Sound Pressure Level        [dB]

    Outputs: 
        SPL  -  Sound Pressure Level        [dB]
    
    Properties Used:
        N/A 
    
    '''
    if SPL.ndim == 1:
        SPL_total = SPL 
    else:
        p_prefs   = 10**(SPL/10)
        SPL_total = 10*np.log10(np.sum(p_prefs, axis = sum_axis))
        
    return SPL_total

## @ingroup Methods-Noise-Fidelity_One-Noise_Tools
def func_SPL_spectra_arithmetic(SPL):
    '''This computes the total SPL spectra from multiple sources 
    using decibel arithmetic  
    
    Assumptions:
        None

    Source:
        None

    Inputs:
        SPL  -  Sound Pressure Level        [dB]

    Outputs: 
        SPL  -  Sound Pressure Level        [dB]
    
    Properties Used:
        N/A 
    
    ''' 
    p_prefs   = 10**(SPL/10)
    SPL_total = 10*np.log10(np.sum(p_prefs, axis = 2))
        
    return SPL_total


pressure_ratio_to_SPL_arithmetic(State, Settings, System):
	#TODO: p_pref_total = [Replace With State, Settings, or System Attribute]

	results = func_pressure_ratio_to_SPL_arithmetic('p_pref_total',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System


SPL_arithmetic(State, Settings, System):
	#TODO: SPL      = [Replace With State, Settings, or System Attribute]
	#TODO: sum_axis = [Replace With State, Settings, or System Attribute]

	results = func_SPL_arithmetic('SPL', 'sum_axis')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System


SPL_spectra_arithmetic(State, Settings, System):
	#TODO: SPL = [Replace With State, Settings, or System Attribute]

	results = func_SPL_spectra_arithmetic('SPL',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System