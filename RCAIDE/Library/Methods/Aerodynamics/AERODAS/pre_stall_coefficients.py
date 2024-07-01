## @ingroup Library-Methods-Aerdoynamics-AERODAS
# RCAIDE/Library/Methods/Aerdoynamics/AERODAS/pre_stall_coefficients.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
# Imports 
# ----------------------------------------------------------------------------------------------------------------------    
# python imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# Pre Stall Coefficients
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Library-Methods-Aerodynamics-AERODAS
def pre_stall_coefficients(state,settings,wing):
    """Uses the AERODAS method to determine prestall parameters for lift and drag for a single wing

    Assumptions:
        None

    Source:
        NASA TR: "Models of Lift and Drag Coefficients of Stalled and Unstalled Airfoils in
        Wind Turbines and Wind Tunnels" by D. A. Spera

    Args:
        state.conditions.aerodynamics.angles.alpha    (numpy.ndarray):  [radians]
        settings.section_zero_lift_angle_of_attack            (float):  [unitless]
        geometry.section.angle_attack_max_prestall_lift       (float):  [unitless]
        geometry.section.zero_lift_drag_coefficient           (float):  [unitless]
        geometry.pre_stall_maximum_drag_coefficient_angle     (float):  [radians]
        geometry.pre_stall_maximum_lift_coefficient           (float):  [unitless]
        geometry.pre_stall_lift_curve_slope                   (float):  [unitless]
        geometry.pre_stall_maximum_lift_drag_coefficient      (float):  [unitless]

    Returns:
        CL1 (numpy.ndarray): coefficient of lift       (numpy.ndarray):  [unitless]
        CD1 (numpy.ndarray): coefficient of drag       (numpy.ndarray):  [unitless]
    """  
    
    # unpack inputs 
    alpha  = state.conditions.aerodynamics.angles.alpha  
    A0     = settings.section_zero_lift_angle_of_attack 
    CL1max = wing.pre_stall_maximum_lift_coefficient
    S1     = wing.pre_stall_lift_curve_slope  
    CD1max = wing.pre_stall_maximum_lift_drag_coefficient
    ACD1   = wing.pre_stall_maximum_drag_coefficient_angle
    ACL1   = wing.section.angle_attack_max_prestall_lift
    CDmin  = wing.section.minimum_drag_coefficient 
    ACDmin = wing.section.minimum_drag_coefficient_angle_of_attack  
        
    # Eqn 6c
    RCL1          = S1*(ACL1-A0)-CL1max
    RCL1[RCL1<=0] = 1.e-16
    
    # Eqn 6d
    N1 = 1.0 + CL1max/RCL1
    
    # Eqn 6a or 6b depending on the alpha
    if wing.vertical == True:
        alpha      = np.zeros_like(alpha)
    CL1            = np.zeros_like(alpha)
    CL1[alpha>A0]  = S1*(alpha[alpha>A0]-A0)-RCL1[alpha>A0]*((alpha[alpha>A0]-A0)/(ACL1[alpha>A0]-A0))**N1[alpha>A0] 
    CL1[alpha<A0]  = S1*(alpha[alpha<A0]-A0)+RCL1[alpha<A0]*((A0-alpha[alpha<A0])/(ACL1[alpha<A0]-A0))**N1[alpha<A0]
     
    # Eqn 7a or 7b depending on the alph
    con      = np.logical_and((2*A0-ACD1)<=alpha,alpha<=ACD1)
    CD1      = np.ones_like(alpha)
    CD1[con] = CDmin[con] + (CD1max[con]-CDmin[con])*((alpha[con] - ACDmin)/(ACD1[con]-ACDmin))**2     
    CD1[np.logical_not(con)] = 0.
    
    # Pack outputs 
    state.conditions.aerodynamics.pre_stall_coefficients[wing.tag].lift =  CL1
    state.conditions.aerodynamics.pre_stall_coefficients[wing.tag].drag =  CD1
    
    return CL1, CD1