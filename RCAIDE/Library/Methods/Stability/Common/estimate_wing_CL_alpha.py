# RCAIDE/Library/Methods/Stability/Common/estimate_wing_CL_alpha.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, M. Clarke

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import numpy as np
from RCAIDE.Library.Methods.Geometry.Planform  import convert_sweep

# ----------------------------------------------------------------------
# estimate_wing_CL_alpha
# ---------------------------------------------------------------------- 
def estimate_wing_CL_alpha(wing,mach):
    """ Estimate the derivative of 3D lift coefficient with respect to angle of attack.

    Assumptions: 
        1) Only applicable for subsonic speeds and may be inaccurate for transonic or supersonic flight.
        2) A correction factor for supersonic flight is included, but may not be completely accurate.
    
    Source:
        1) DATCOM 
        2) Sectional lfit curve slope at M = 0 is 6.18 is based on Roskam Airplane Design Part VI, Table 8.1 
         
    Args:
        wing           (dict): wing data structure [-] 
        mach  (numpy.ndarray): flight Mach number  [unitless]

    Returns:
        cL_alpha   (numpy.ndarray): derivative of lift coefficient with respect to angle of attack [unitless]


    """          
    if 'effective_aspect_ratio' in wing:
        ar = wing.effective_aspect_ratio
    elif 'extended' in wing:
        if 'aspect_ratio' in wing.extended:
            ar = wing.extended.aspect_ratio
        else:
            ar = wing.aspect_ratio
    else:
        ar = wing.aspect_ratio    
        
    # convert wing sweep 
    half_chord_sweep = convert_sweep(wing,0.25,0.5) 
    
    # Lift curve slope 
    cla = 6.13         

    # Initlaize arrays 
    cL_alpha = np.ones_like(mach)
    Beta     = np.ones_like(mach)
    k        = np.ones_like(mach)
    cla_M    = np.ones_like(mach)

    #Compute k correction factor for Mach number     
    Beta[mach<1.]  = (1.0-mach[mach<1.]**2.0)**0.5
    Beta[mach>1.]  = (mach[mach>1.]**2.0-1.0)**0.5
    cla_M[mach<1.] = cla/Beta[mach<1.]
    cla_M[mach>1.] = 4.0/Beta[mach>1.]
    k              = cla_M/(2.0*np.pi/Beta)
    
    # Compute aerodynamic surface 3D lift curve slope using the DATCOM formula
    cL_alpha =(2.0*np.pi*ar/(2.0+((ar**2.0*(Beta*Beta)/(k*k))*(1.0+(np.tan(half_chord_sweep))**2.0/(Beta*Beta))+4.0)**0.5))
    
    return cL_alpha
