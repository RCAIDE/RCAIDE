# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/wave_drag.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports   
import numpy as np
from RCAIDE.Library.Components.Wings import Main_Wing

# ----------------------------------------------------------------------------------------------------------------------
#  Wave Drag 
# ----------------------------------------------------------------------------------------------------------------------
def wave_drag(conditions,wing):
    """Computes wave drag due to lift

    Assumptions:
        The main wing is the primary lift contributor

    Source:
        Yoshida, Kenji. "Supersonic drag reduction technology in the scaled supersonic 
        experimental airplane project by JAXA."

    Args:
        conditions.freestream.mach_number         (numpy.ndarray): mach number       [unitless]
        conditions.aerodynamics.coefficients.lift (numpy.ndarray): lift coefficient  [unitless]
        wing.spans.projected                               (float): projected span   [m]
        wing.total_length                                  (float): wing root length [m]
        wing.aspect_ratio                                  (float): aspect ratio     [-]

    Returns:
        wave_drag_lift                            (numpy.ndarray): wave drag         [unitless] 
    """  
 
    # Unpack
    freestream  = conditions.freestream 
    Mach        = freestream.mach_number  
    
    # Lift coefficient 
    if isinstance(wing,Main_Wing):
        CL = conditions.aerodynamics.coefficients.lift.total 
        l  = np.maximum(wing.total_length,wing.chords.root)        
    else:
        CL = np.zeros_like(conditions.aerodynamics.coefficients.lift.total)
        l  = np.maximum(wing.total_length,wing.chords.root) 
 
    s    = wing.spans.projected / 2
    AR   = wing.aspect_ratio
    p    = 2/AR*s/l
    beta = np.sqrt(Mach[Mach >= 1.01]**2-1) 
    Kw   = (1+1/p)*func(beta*s/l)/(2*beta**2*(s/l)**2)
    
    # Ignore area comparison since this is full vehicle CL
    CDwl           = CL[Mach >= 1.01]**2 * (beta**2/np.pi*p*(s/l)*Kw)
    wave_drag_lift = np.zeros_like(Mach)
    wave_drag_lift[Mach >= 1.01] = CDwl


    return wave_drag_lift

def func(x):
    """Helper function for lift wave drag computations.

    Assumptions:
        None

    Source:
        Yoshida, Kenji. "Supersonic drag reduction technology in the scaled supersonic 
        experimental airplane project by JAXA."

    Args:
        x (float): variable      [unitless]

    Returns:
        ret (float): variable    [unitless] 
    """   
    ret = np.zeros_like(x) 
    ret[x > 0.178] = 0.4935 - 0.2382*x[x > 0.178] + 1.6306*x[x > 0.178]**2 - \
        0.86*x[x > 0.178]**3 + 0.2232*x[x > 0.178]**4 - 0.0365*x[x > 0.178]**5 - 0.5
    
    return ret