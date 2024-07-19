# RCAIDE/Methods/Aerodynamics/Common/Drag/compressibility_drag_wing.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
from RCAIDE.Framework.Core import Data    
 
# package imports
import numpy as np  

# ----------------------------------------------------------------------------------------------------------------------  
#   Compressibility Drag for Wings 
# ----------------------------------------------------------------------------------------------------------------------   
def compressibility_drag_wing(state,settings,wing):
    """Computes compressibility drag for a wing

    Assumptions:
         1. Subsonic to low transonic
         2. Supercritical airfoil

    Source:
         1. Shevell, Richard Shepherd. Fundamentals of flight. Pearson Education India, 1989.
         2. Stanford AA241 A/B Course Notes

    Args:
        state    (dict): flight conditions    [-]
        settings (dict): analyses settings    [-]
        wing     (dict): wing diata structure [-]

    Returns:
        None
    """ 
    
    # unpack 
    mach       = state.conditions.freestream.mach_number 
    cl_w       = state.conditions.aerodynamics.coefficients.lift.compressible_wings[wing.tag]   
    t_c_w      = wing.thickness_to_chord
    sweep_w    = wing.sweeps.quarter_chord
    cos_sweep  = np.cos(sweep_w)

    # get effective Cl and thickness to chord
    cl         = cl_w / (cos_sweep*cos_sweep)
    tc         = t_c_w /(cos_sweep)

    # compressibility drag based on regressed fits from Stanford AA241 Notes 
    mcc_cos_ws = 0.922321524499352       \
               - 1.153885166170620*tc    \
               - 0.304541067183461*cl    \
               + 0.332881324404729*tc*tc \
               + 0.467317361111105*tc*cl \
               + 0.087490431201549*cl*cl
        
    # crest-critical mach number, corrected for wing sweep
    mcc = mcc_cos_ws / cos_sweep
    
    # divergence mach number
    MDiv = mcc * ( 1.02 + 0.08*(1 - cos_sweep) )
    
    # divergence ratio
    mo_mc = mach/mcc
    
    # compressibility correlation from Shevell
    dcdc_cos3g = 0.0019*mo_mc**14.641
    
    # compressibility drag
    cd_c = dcdc_cos3g * cos_sweep*cos_sweep*cos_sweep

    # Store results 
    wing_results = Data(
        total                    = cd_c    ,
        thickness_to_chord        = tc      , 
        wing_sweep                = sweep_w , 
        crest_critical            = mcc     ,
        divergence_mach           = MDiv    ,
    )
    state.conditions.aerodynamics.coefficients.drag.compressible[wing.tag] = wing_results
    
    return 
