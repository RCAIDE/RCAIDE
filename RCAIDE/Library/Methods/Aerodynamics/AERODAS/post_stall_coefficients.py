# RCAIDE/Library/Methods/Aerdoynamics/AERODAS/post_stall_coefficients.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# Imports 
# ----------------------------------------------------------------------------------------------------------------------
from RCAIDE.Reference.Core import Units

# python imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# Post Stall Coefficients
# ----------------------------------------------------------------------------------------------------------------------    
def post_stall_coefficients(state,settings,wing):
    """Uses the AERODAS method to determine poststall parameters for lift and drag for a single wing

    Assumptions:
        None

    Source:
        NASA TR: "Models of Lift and Drag Coefficients of Stalled and Unstalled Airfoils in
        Wind Turbines and Wind Tunnels" by D. A. Spera

    Args:
        state.conditions.aerodynamics.angles.alpha    (numpy.ndarray:  [radians]
        settings.section_zero_lift_angle_of_attack           (float):  [radians]
        wing.aspect_ratio                                    (float):  [unitless]
        wing.thickness_to_chord                              (float):  [unitless]
        wing.section.angle_attack_max_prestall_lift          (float):  [radians]
        wing.pre_stall_maximum_lift_drag_coefficient         (float):  [unitless]
        wing.pre_stall_maximum_drag_coefficient_angle        (float):  [unitless] 

    Returns:
        CL2 (coefficient of lift)                    (numpy.ndarray):  [unitless]
        CD2 (coefficient of drag)                    (numpy.ndarray):  [unitless] 
    """  
    
    # unpack inputs 
    A0     = settings.section_zero_lift_angle_of_attack
    AR     = wing.aspect_ratio
    t_c    = wing.thickness_to_chord
    ACL1   = wing.section.angle_attack_max_prestall_lift 
    CD1max = wing.pre_stall_maximum_lift_drag_coefficient
    ACD1   = wing.pre_stall_maximum_drag_coefficient_angle
    alpha  = state.conditions.aerodynamics.angles.alpha 
            
    # Eqn 9a and b
    F1        = 1.190*(1.0-(t_c*t_c))
    F2        = 0.65 + 0.35*np.exp(-(9.0/AR)**2.3)
    
    # Eqn 10b and c
    G1        = 2.3*np.exp(-(0.65*t_c)**0.9)
    G2        = 0.52 + 0.48*np.exp(-(6.5/AR)**1.1)
    
    # Eqn 8a and b
    CL2max    = F1*F2
    CD2max    = G1*G2
    
    # Eqn 11d
    RCL2      = 1.632-CL2max
    
    # Eqn 11e
    N2        = 1.0 + CL2max/RCL2
    
    # Eqn 11a,b,c
    if wing.vertical == True:
        alpha = np.zeros_like(alpha)    
    con2      = np.logical_and(ACL1<=alpha,alpha<=(92.0*Units.deg))
    con3      = alpha>=(92.0*Units.deg)
    CL2       = np.zeros_like(alpha) 
    CL2[con2] = -0.032*(alpha[con2]/Units.deg-92.0) - RCL2*((92.*Units.deg-alpha[con2])/(51.0*Units.deg))**N2
    CL2[con3] = -0.032*(alpha[con3]/Units.deg-92.0) + RCL2*((alpha[con3]-92.*Units.deg)/(51.0*Units.deg))**N2
    
    # Invert lift for negative alpha  
    alphan    = -alpha+2*A0
    con4      = np.logical_and(0<alphan, alphan<ACL1)
    con5      = np.logical_and(ACL1<=alphan, alphan<=(92.0*Units.deg))
    con6      = alphan>=(92.0*Units.deg)
    CL2[con4] = 0.
    CL2[con5] = 0.032*(alphan[con5]/Units.deg-92.0) + RCL2*((92.*Units.deg-alphan[con5])/(51.0*Units.deg))**N2
    CL2[con6] = 0.032*(alphan[con6]/Units.deg-92.0) - RCL2*((alphan[con6]-92.*Units.deg)/(51.0*Units.deg))**N2
    
    # Eqn 12a  
    con8      = alpha>ACD1
    CD2       = np.zeros_like(alpha) 
    CD2[con8] = CD1max[con8] + (CD2max - CD1max[con8]) * np.sin((alpha[con8]-ACD1[con8])/(np.pi/2-ACD1[con8]))
    
    # Invert drag for negative alpha 
    alphan    = -alpha + 2*A0
    con9      = np.logical_and((2*A0-ACL1)<alphan,alphan<ACL1)
    con10     = alphan>=ACD1
    CD2[con9] = 0.0
    CD2[con10]= CD1max[con10] + (CD2max - CD1max[con10]) * np.sin((alphan[con10]-ACD1[con10])/(np.pi/2-ACD1[con10]))        
        
    # Pack results  
    state.conditions.aerodynamics.post_stall_coefficients[wing.tag].lift =  CL2
    state.conditions.aerodynamics.post_stall_coefficients[wing.tag].draf =  CD2
    
    return CL2, CD2