# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/drag_divergence.py 
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports    
from RCAIDE.Library.Components.Wings import Main_Wing 

# package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Drag Divergence
# ---------------------------------------------------------------------------------------------------------------------- 
def drag_divergence(Mc_ii,wing,cl,Sref):
    """Use drag divergence mach number to determine drag for subsonic speeds

    Assumptions:
        Concorde fit is used for supersonic calculations 

    Source:
        1. Shevell, Richard Shepherd. Fundamentals of flight. Pearson Education India, 1989.
        2. Stanford AA241 A/B Course Notes
        3. Concorde data can be found in "Supersonic drag reduction technology in the scaled supersonic 
           experimental airplane project by JAXA" by Kenji Yoshida

    Args:
        Mc_ii   (float): Mach number                [unitless] 
        wing     (dict): wing data structure        [unitless] 
        cl      (float): lift coefficient           [unitless] 
        Sref    (float): reference area             [unitless] 

    Returns:
        cd_sup  (float): supersonic drag             [unitless]
        mcc     (float): Crest-critical mach number  [unitless]
        MDiv    (float):  Divergence mach number     [unitless] 

    """          
    # Check if the wing is designed for high subsonic cruise 
    if wing.high_mach:  
        MDiv = 0.98* np.ones_like(Mc_ii) 
        mcc  = 0.95* np.ones_like(Mc_ii)  
    else: 
        t_c_w   = wing.thickness_to_chord
        sweep_w = wing.sweeps.quarter_chord

        # wing is the main wing, other wings are assumed to have no lift 
        if isinstance(wing, Main_Wing):
            cl_w = cl
        else:
            cl_w = 0

        # Get effective Cl and sweep
        cos_sweep = np.cos(sweep_w)
        tc        = t_c_w / cos_sweep
        cl        = cl_w / (cos_sweep*cos_sweep)

        # Compressibility drag based on regressed fits  
        mcc_cos_ws = 0.922321524499352  - 1.153885166170620*tc - 0.304541067183461*cl + 0.332881324404729*tc*tc  + 0.467317361111105*tc*cl   + 0.087490431201549*cl*cl

        # Crest-critical mach number, corrected for wing sweep
        mcc = mcc_cos_ws / cos_sweep

        # Divergence mach number
        MDiv = mcc * ( 1.02 + 0.08*(1 - cos_sweep) )        

    # Divergence ratio
    mo_mc = Mc_ii/mcc

    # Compressibility correlation 
    dcdc_cos3g = 0.0019*mo_mc**14.641 

    # Sweep correlation cannot be used if the wing has a high mach design
    if wing.high_mach:
        cd_sup = (dcdc_cos3g )*wing.areas.reference/Sref    
    else:
        cd_sup = (dcdc_cos3g * (np.cos(sweep_w))**3 )*wing.areas.reference/Sref
    
    # Change empty format to avoid errors in assignment of returned values
    if np.shape(cd_sup) == (0,0):
        cd_sup = np.reshape(cd_sup,[0,1]) 
        mcc    = np.reshape(mcc,[0,1]) 
        MDiv   = np.reshape(MDiv,[0,1]) 

    return (cd_sup,mcc,MDiv)
