## @ingroup Library-Methods-Noise-Metrics  
# RCAIDE/Library/Methods/Noise/Metrics/A_weighting_metric.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------  
 
# Python package imports   
import numpy as np  
    
# ----------------------------------------------------------------------------------------------------------------------  
#  A_weighting_metric
# ----------------------------------------------------------------------------------------------------------------------     
## @ingroup Library-Methods-Noise-Metrics
def A_weighting_metric(SPL,f): 
    """This method calculates the A-weighted SPL given its stectra
    
    Assumptions:
        None

    Source:
        IEC 61672-1:2013 Electroacoustics - Sound level meters - Part 1: Specifications. IEC. 2013.

    Args:
        SPL     - Sound Pressure Level             [dB] 

    Returns:  
        SPL_dBA - A-weighted Sound Pressure Level  [dBA]  
    """    
    Ra_f       = ((12194**2)*(f**4))/ (((f**2)+(20.6**2)) * ((f**2)+(12194**2)) * (((f**2) + 107.7**2)**0.5)*(((f**2)+ 737.9**2)**0.5)) 
    A_f        =  2.0  + 20*np.log10(Ra_f) 
    SPL_dBA    = SPL + A_f
    return SPL_dBA
