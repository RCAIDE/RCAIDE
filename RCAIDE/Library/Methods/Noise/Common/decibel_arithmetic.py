## @ingroup Library-Methods-Noise-Common 
# RCAIDE/Library/Methods/Noise/Common/decibel_arithmetic.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# Python package imports   
import numpy as np  
    
# ----------------------------------------------------------------------------------------------------------------------  
#  pressure_ratio_to_SPL_arithmetic
# ----------------------------------------------------------------------------------------------------------------------      
## @ingroup Library-Methods-Noise-Common  
def pressure_ratio_to_SPL_arithmetic(p_pref_total):
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
    SPL_total = 10*np.log10(np.nansum(p_pref_total, axis = 3))
    return SPL_total


    
# ----------------------------------------------------------------------------------------------------------------------  
#  SPL_arithmetic
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Library-Methods-Noise-Common
def SPL_arithmetic(SPL, sum_axis = 2):
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
        SPL_total = 10*np.log10(np.nansum(p_prefs, axis = sum_axis))
        
    return SPL_total


def _pressure_ratio_to_SPL_arithmetic(State, Settings, System):
	'''
	Framework version of pressure_ratio_to_SPL_arithmetic.
	Wraps pressure_ratio_to_SPL_arithmetic with State, Settings, System pack/unpack.
	Please see pressure_ratio_to_SPL_arithmetic documentation for more details.
	'''

	#TODO: p_pref_total = [Replace With State, Settings, or System Attribute]

	results = pressure_ratio_to_SPL_arithmetic('p_pref_total',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System


def _SPL_arithmetic(State, Settings, System):
	'''
	Framework version of SPL_arithmetic.
	Wraps SPL_arithmetic with State, Settings, System pack/unpack.
	Please see SPL_arithmetic documentation for more details.
	'''

	#TODO: SPL      = [Replace With State, Settings, or System Attribute]
	#TODO: sum_axis = [Replace With State, Settings, or System Attribute]

	results = SPL_arithmetic('SPL', 'sum_axis')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System