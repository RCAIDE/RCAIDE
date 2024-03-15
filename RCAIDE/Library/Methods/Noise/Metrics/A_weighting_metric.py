## @ingroup Library-Methods-Noise-Metrics  
# RCAIDE/Library/Methods/Noise/Metrics/A_weighting_metric.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke  

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
        N/A

    Source:
        IEC 61672-1:2013 Electroacoustics - Sound level meters - Part 1: Specifications. IEC. 2013.

    Inputs:
        SPL     - Sound Pressure Level             [dB] 

    Outputs: [dB]
        SPL_dBA - A-weighted Sound Pressure Level  [dBA] 

    Properties Used:
        N/A 
        
    """    
    Ra_f       = ((12194**2)*(f**4))/ (((f**2)+(20.6**2)) * ((f**2)+(12194**2)) * (((f**2) + 107.7**2)**0.5)*(((f**2)+ 737.9**2)**0.5)) 
    A_f        =  2.0  + 20*np.log10(Ra_f) 
    SPL_dBA    = SPL + A_f
    return SPL_dBA



def _A_weighting_metric(State, Settings, System):
	'''
	Framework version of A_weighting_metric.
	Wraps A_weighting_metric with State, Settings, System pack/unpack.
	Please see A_weighting_metric documentation for more details.
	'''

	#TODO: SPL = [Replace With State, Settings, or System Attribute]
	#TODO: f   = [Replace With State, Settings, or System Attribute]

	results = A_weighting_metric('SPL', 'f')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System