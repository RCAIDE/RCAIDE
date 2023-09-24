## @ingroup Methods-Airfoil
# post_stall_coefficients.py
# 
# Created:  Aug 2023, R. Erhard
# Modified:

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import numpy as np
from Legacy.trunk.S.Core import Units, Data

# ----------------------------------------------------------------------
#  Post Stall Coefficients
# ----------------------------------------------------------------------

## @ingroup Methods-Airfoil
def post_stall_coefficients(state, settings, geometry, apply_stall_transformation=True):
    """Uses the AERODAS method to determine poststall parameters for lift and drag for a single wing

    Assumptions:
    None

    Source:
    NASA TR: "Models of Lift and Drag Coefficients of Stalled and Unstalled Airfoils in
      Wind Turbines and Wind Tunnels" by D. A. Spera

    Inputs:
    settings.section_zero_lift_angle_of_attack      [radians]
    geometry.
      aspect_ratio                                  [Unitless]
      thickness_to_chord                            [Unitless]
      section.angle_attack_max_prestall_lift        [radians]
      pre_stall_maximum_lift_drag_coefficient       [Unitless]
      pre_stall_maximum_drag_coefficient_angle      [Unitless]
    state.conditions.aerodynamics.angle_of_attack   [radians]
    extrapolation_method   -  Method used for extrapolation to deep stall polar data
       'aerodas' - uses Spera's empirical functions for deep stall model 
       'aerodas_smooth' - uses aerodas with a stall region smoothing based on Montgomerie (2004)
      

    Outputs:
    CL2 (coefficient of lift)                       [Unitless]
    CD2 (coefficient of drag)                       [Unitless]
    (packed in state.conditions.aerodynamics.post_stall_coefficients[geometry.tag])

    Properties Used:
    N/A
    """  
    
    # unpack inputs
    wing   = geometry
    A0     = settings.section_zero_lift_angle_of_attack
    AR     = wing.aspect_ratio
    t_c    = wing.thickness_to_chord
    ACL1   = wing.section.angle_attack_max_prestall_lift 
    CL1max = wing.pre_stall_maximum_lift_coefficient
    CD1max = wing.pre_stall_maximum_drag_coefficient
    ACD1   = wing.pre_stall_maximum_drag_coefficient_angle
    alpha  = state.conditions.aerodynamics.angle_of_attack
    
    # Calculate the maximum post-stall lift and drag based on airfoil geometry
    CL2max, CD2max = get_post_stall_max_lift_drag(t_c, AR)
    
    # Generate the post-stall lift and drag curves
    CL2 = generate_post_stall_lift(alpha, A0, ACL1, CL2max)
    CD2 = generate_post_stall_drag(alpha, A0, ACL1, ACD1, CD1max, CD2max)
    
    # Apply transformation function to smooth the transition between pre-stall and post-stall
    if apply_stall_transformation:
        CL2 = apply_stall_region_transformation_function(alpha, A0, ACL1, CL1max, CL2)
    
    # Pack outputs
    wing_result = Data(
        lift_coefficient = CL2,
        drag_coefficient = CD2
        )
    
    state.conditions.aerodynamics.post_stall_coefficients[wing.tag] =  wing_result
    
    return CL2, CD2

def get_post_stall_max_lift_drag(t_c, AR):
    # Equation 9a and b
    F1 = 1.190 * (1.0 - (t_c * t_c))
    F2 = 0.65 + 0.35 * np.exp(-(9.0 / AR)**2.3)
    
    # Equation 10b and c
    G1 = 2.3 * np.exp(-(0.65 * t_c)**0.9)
    G2 = 0.52 + 0.48*np.exp(-(6.5 / AR)**1.1)
    
    # Equation 8a and b
    CL2max = F1 * F2
    CD2max = G1 * G2
    return CL2max, CD2max

def generate_post_stall_lift(alpha, A0, ACL1, CL2max):
    """
    Spera's model to compute the variation of post-stall lift with angle of attack.
    
    Inputs
       alpha  -  angles of attack                                [rad]
       A0     -  zero lift angle of attack                       [rad]
       ACL1   -  angle of maximum pre-stall lift coefficient     [rad]
       CL2max -  maximum calculated post-stall lift coefficient  [-]
    Outputs
       CL2    -  post-stall lift coefficient values corresponding to alpha vector
    
    """
    # Equation 11d
    RCL2      = 1.632 - CL2max
    
    # Equation 11e
    N2        = 1 + CL2max / RCL2
    
    # Equation 11a,b,c
    con1 = lambda a: np.logical_and(0 < a, a < ACL1)                   # Pre-stall region (not included in post-stall curve)
    con2 = lambda a: np.logical_and(ACL1 <= a, a <= (92.0*Units.deg))  # First post-stall region before zero-crossing
    con3 = lambda a: a >= (92.0 * Units.deg)                           # Second post-stall region after zero-crossing
    
    f1 = lambda a: -0.032 * (a / Units.deg - 92.0) - RCL2 * ((92.*Units.deg - a) / (51.0 * Units.deg))**N2
    f2 = lambda a: -0.032 * (a / Units.deg - 92.0) + RCL2 * ((a - 92.*Units.deg) / (51.0 * Units.deg))**N2
    f = lambda a: np.piecewise(a, [con1(a), con2(a), con3(a)], [0, f1, f2])

    alphan = -alpha + 2*A0
    n_ids = np.logical_or(con2(alphan), con3(alphan))
    CL2 = f(alpha)
    CL2[n_ids] = -f(alphan)[n_ids]
    
    return CL2

def generate_post_stall_drag(alpha, A0, ACL1, ACD1, CD1max, CD2max):
    """
    Spera's model to compute the variation of post-stall drag with angle of attack.
    
    Inputs
       alpha  -  angles of attack                                [rad]
       A0     -  zero lift angle of attack                       [rad]
       ACL1   -  angle of maximum pre-stall lift coefficient     [rad]
       ACD1   -  angle of maximum pre-stall drag coefficient     [rad]
       CL2max -  maximum calculated post-stall lift coefficient  [-]
       CD2max -  maximum calculated post-stall drag coefficient  [-]
    Outputs
       CD2    -  post-stall drag coefficient values corresponding to alpha vector
    
    """    
    # Equation 12a 
    con1      = np.logical_and((2*A0-ACL1)<alpha, alpha<ACL1)
    con2      = alpha>=ACD1
    CD2       = np.zeros_like(alpha)
    CD2[con1] = 0.
    CD2[con2] = CD1max[con2] + (CD2max - CD1max[con2]) * np.sin( ( (alpha[con2]-ACD1[con2])/(np.pi/2-ACD1[con2])) * np.pi/2)
    
    # If alpha is negative flip things for drag
    alphan    = -alpha + 2*A0
    con1      = np.logical_and((2*A0-ACD1)<alphan,alphan<ACL1)
    con2      = alphan>=ACD1
    CD2[con1] = 0.
    CD2[con2] = CD1max[con2] + (CD2max - CD1max[con2]) * np.sin( ( (alphan[con2]-ACD1[con2])/(np.pi/2-ACD1[con2]))  * np.pi/2)       
    return CD2    

def apply_stall_region_transformation_function(alpha, A0, ACL1, CL1max, CL2):
    """
    Uses a transformation function that transforms CL and is used for interpolation between the 
    pre-stall and deep-stall regimes. The transformation function follows that of Montgomerie, B., 2004.
    This is applied to interpolate between the deep stall region (Spera's model) and pre-stall region (Xfoil).
    
    Inputs
       alpha  -  angles of attack                                [rad]
       A0     -  zero lift angle of attack                       [rad]
       ACL1   -  angle of maximum pre-stall lift coefficient     [rad]
       CL1max -  maximum pre-stall lift coefficient              [-]
       CL2    -  post-stall lift coefficient at alpha            [-]
       CD2    -  post-stall drag coefficient at alpha            [-]
    Outputs
       CL2    -  post-stall lift coefficient at alpha            [-]
       CD2    -  post-stall drag coefficient at alpha            [-]
    """
    # Model parameters
    k = 0.001
    a_range = 20 * Units.deg
    alphan = -alpha + 2*A0
    
    # Set start and end angles indicating stall regions
    aL_p_i = ACL1[0]
    aL_n_i = ACL1[0] - 2 * A0
    aL_p_f = aL_p_i + a_range
    
    CL_i = CL1max[0]
    CL_f = CL2[np.argmin(abs(alpha - aL_p_f))]

    # Create transformation function
    f_transform = lambda delta: 1 / (1 + k * delta**4)
    
    # Apply transformation function to CL2 positive post-stall
    con = lambda a: np.logical_and(a > aL_p_i, a < aL_p_f) # Mid-stall region
    
    f_pos = f_transform( (alpha - aL_p_i) / Units.deg )[con(alpha)]
    f_neg = f_transform( (alphan - aL_n_i) / Units.deg )[con(alphan)]
    
    # Apply to lift
    CL2[con(alpha)] = CL_f + (CL_i-CL_f) * f_pos
    CL2[con(alphan)] = -(CL_f + (CL_i-CL_f) * f_neg)

    return CL2