## @ingroup Library-Methods-Noise-Frequency_Domain_Buildup-Rotor
# RCAIDE/Library/Methods/Noise/Frequency_Domain_Buildup/Rotor/noise_directivities.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke  

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# Python Package imports  
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------
# Compute Noise Directivities  
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Noise-Frequency_Domain_Buildup-Rotor 
def noise_directivities(Theta_er,Phi_er,cos_zeta_r,M_tot):
    '''This computes the laminar boundary layer compoment of broadband noise using the method outlined by the 
    Brooks, Pope and Marcolini (BPM) Model
    
    Assumptions:
        BPM models assumes a naca 0012 airfol  
        
    Source:  
        BPM Model:  Brooks, Thomas F., D. Stuart Pope, and Michael A.
        Marcolini. Airfoil self-noise and prediction. No. L-16528. 1989.
    
    Inputs:  
       Theta_e      - Radiation angle with respect to free stream x (chordwise) [rad]
       Phi_e        - Radiation angle with respect to free stream y (spanwise)  [rad]
       M_c          - Convection Mach number                                    [-]  
       M            - Mach number                                               [-] 
    
    Outputs 
       Dbar_h       - high frequency directivity term                           [-]
       Dbar_l       - low frequency directivity term                            [-] 
       
    Properties Used:
       N/A   
    '''      
    Dbar_h   = (2*(np.sin(Theta_er/2)**2)*((np.sin(Phi_er))**2) )/((1 - M_tot*cos_zeta_r)**4)  # eqn 20 Brooks & Burley
    Dbar_l   = ((np.sin(Theta_er)**2)*((np.sin(Phi_er))**2) )/((1 - M_tot*cos_zeta_r)**4)  # eqn 19 Brooks & Burley  
    return Dbar_h,Dbar_l 


def _noise_directivities(State, Settings, System):
	'''
	Framework version of noise_directivities.
	Wraps noise_directivities with State, Settings, System pack/unpack.
	Please see noise_directivities documentation for more details.
	'''

	#TODO: Theta_er   = [Replace With State, Settings, or System Attribute]
	#TODO: Phi_er     = [Replace With State, Settings, or System Attribute]
	#TODO: cos_zeta_r = [Replace With State, Settings, or System Attribute]
	#TODO: M_tot      = [Replace With State, Settings, or System Attribute]

	results = noise_directivities('Theta_er', 'Phi_er', 'cos_zeta_r', 'M_tot')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System