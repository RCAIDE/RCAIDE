

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

# package imports
import numpy as np


# ----------------------------------------------------------------------
#  Compressible Mixed Flat Plate
# ----------------------------------------------------------------------
def compressible_mixed_flat_plate(Re,Ma,Tc,xt):
    """Computes the coefficient of friction for a flat plate given the 
    input parameters. Also returns the correction terms used in the
    computation.

    Assumptions:
    Reynolds number between 10e5 and 10e9
    xt between 0 and 1

    Source:
    adg.stanford.edu (Stanford AA241 A/B Course Notes)

    Inputs:
    Re (Reynolds number)                                             [Unitless]
    Ma (Mach number)                                                 [Unitless]
    Tc (temperature)                                                 [K]
    xt (turbulent transition point as a proportion of chord length)  [Unitless]

    Outputs:
    cf_comp (coefficient of friction)                                [Unitless]
    k_comp (compressibility correction)                              [Unitless]
    k_reyn (Reynolds number correction)                              [Unitless]

    Properties Used:
    N/A
    """     
    
    if xt < 0.0 or xt > 1.0:
        raise ValueError("Turbulent transition must be between 0 and 1")

    Rex = Re*xt
    Rex[Rex==0.0] = 0.0001

    theta = 0.671*xt/(Rex**0.5)
    xeff  = (27.78*theta*Re**0.2)**1.25
    Rext  = Re*(1-xt+xeff)
    
    #cf_turb  = 0.455/(np.log10(Rext)**2.58) # Schlichting empircal formula for turbulent flat plate. note that this correlation is meant for smooth surfaces.

    # Turbulent flat plate correlation from Shevell's Fundamentals of Flight. Accounts for typical roughness of a transport aircraft
    y = np.array([0.01273, 0.0090077, 0.0058721317, 0.00716019, 0.0049416, 0.003744045, 0.00316321, 0.002506763, 0.002064, 0.0016604122])
    x = np.array([10000, 115300, 675100, 281300, 1492600, 6040200, 14920400, 58584300, 193593000, 897594100])
    cf_turb = np.interp(Rext, x, y) # Data is from Figure 11.2 of Shevell's Fundamentals of Flight.
    cf_lam   = 1.328/(Rex**0.5)
    
    if xt > 0.0:
        cf_start = np.interp(Re*xeff, x, y)  
    else:
        cf_start = 0.0
    
    cf_inc = cf_lam*xt + cf_turb*(1-xt+xeff) - cf_start*xeff
    
    # compressibility correction
    Tw = Tc * (1. + 0.178*Ma*Ma)
    Td = Tc * (1. + 0.035*Ma*Ma + 0.45*(Tw/Tc - 1.))
    k_comp = (Tc/Td) 
    
    # reynolds correction
    Rd_w   = Re * (Td/Tc)**1.5 * ( (Td+216.) / (Tc+216.) )
    k_reyn = (Re/Rd_w)**0.2
    
    # apply corrections
    cf_comp = cf_inc * k_comp * k_reyn
    
    return cf_comp, k_comp, k_reyn