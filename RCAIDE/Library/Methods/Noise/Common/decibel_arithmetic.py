## @ingroup Library-Methods-Noise-Common 
# RCAIDE/Library/Methods/Noise/Common/decibel_arithmetic.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke  

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

    Args:
        Pressure Ratios       [unitless]

    Returns: 
        Sound Pressure Level  [decibel] 
    
    '''
    SPL_total = 10*np.log10(np.nansum(p_pref_total, axis = 3))
    return SPL_total
 
    
# ----------------------------------------------------------------------------------------------------------------------  
#  SPL_arithmetic
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Library-Methods-Noise-Common
def SPL_arithmetic(SPL, sum_axis = 2):
    '''This computes the total SPL from multiple sources using decibel arithmetic  
    
    Assumptions:
        None

    Source:
        None

    Args:
        SPL  -  Sound Pressure Level        [dB]

    Returns: 
        SPL  -  Sound Pressure Level        [dB]  
    '''
    if SPL.ndim == 1:
        SPL_total = SPL 
    else:
        p_prefs   = 10**(SPL/10)
        SPL_total = 10*np.log10(np.nansum(p_prefs, axis = sum_axis))
        
    return SPL_total