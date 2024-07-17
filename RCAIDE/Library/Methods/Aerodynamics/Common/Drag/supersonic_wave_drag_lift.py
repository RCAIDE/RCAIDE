# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/supersonic_compressibility_drag_total.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
   
from RCAIDE.Library.Components.Wings          import Main_Wing 

# package imports
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
#  Supersonic Wave Draf Due to Lift 
# ----------------------------------------------------------------------------------------------------------------------  
def supersonic_wave_drag_lift(conditions,configuration,wing):
    """Computes wave drag due to lift

    Assumptions:
    Main wing is the primary lift contributor

    Source:
    Yoshida, Kenji. "Supersonic drag reduction technology in the scaled supersonic 
    experimental airplane project by JAXA."

    Args:
    conditions.freestream.mach_number        [Unitless]
    conditions.aerodynamics.lift_coefficient [Unitless]
    wing.spans.projected                     [m]
    wing.total_length                        [m]
    wing.aspect_ratio                        [-]

    Returns:
    wave_drag_lift                           [Unitless]

    Properties Used:
    N/A
    """  

    # Unpack
    freestream  = conditions.freestream 
    Mach        = freestream.mach_number * 1.0
    
    # Lift coefficient
    if isinstance(wing,Main_Wing):
        CL = conditions.aerodynamics.coefficients.lift.total
    else:
        CL = np.zeros_like(conditions.aerodynamics.coefficients.lift.total)

    # JAXA method
    s    = wing.spans.projected / 2
    l    = wing.total_length
    AR   = wing.aspect_ratio
    p    = 2/AR*s/l
    beta = np.sqrt(Mach[Mach >= 1.01]**2-1)
    
    Kw = (1+1/p)*fw(beta*s/l)/(2*beta**2*(s/l)**2)
    
    # Ignore area comparison since this is full vehicle CL
    CDwl           = CL[Mach >= 1.01]**2 * (beta**2/np.pi*p*(s/l)*Kw)
    wave_drag_lift = np.zeros_like(Mach)
    wave_drag_lift[Mach >= 1.01] = CDwl

    return wave_drag_lift

def fw(x):
    """Helper function for lift wave drag computations.

    Assumptions:
    N/A

    Source:
    Yoshida, Kenji. "Supersonic drag reduction technology in the scaled supersonic 
    experimental airplane project by JAXA."

    Args:
    x    [Unitless]

    Returns:
    ret  [Unitless] 
    """  
    
    ret = np.zeros_like(x)
    
    ret[x > 0.178] = 0.4935 - 0.2382*x[x > 0.178] + 1.6306*x[x > 0.178]**2 - \
        0.86*x[x > 0.178]**3 + 0.2232*x[x > 0.178]**4 - 0.0365*x[x > 0.178]**5 - 0.5
    
    return ret