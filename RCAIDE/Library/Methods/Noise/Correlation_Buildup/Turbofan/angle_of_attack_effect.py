## @ingroup Library-Methods-Noise-Correlation_Buildup-Engine 
# RCAIDE/Library/Methods/Noise/Correlation_Buildup/Engine/angle_of_attack_effect.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke  

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
        None

    Source:
        SAE Model
    
    Args:   
        AoA           angle of attack         [rad]
        Mach_aircraft mach number of aircraft [unitless]
        theta_m       emission angle          [rad]                
    
    Returns:
        ATK_m         angle of attack effect  [unitless]   
    """

    # Angle of attack effect
    ATK_m = 0.5*AoA*Mach_aircraft*((1.8*theta_m/np.pi)-0.6)**2

    return ATK_m
