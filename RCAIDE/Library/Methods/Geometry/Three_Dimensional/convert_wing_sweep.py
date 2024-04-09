## @ingroup Library-Methods-Geometry-Three_Dimensional
# RCAIDE/Library/Methods/Geometry/Three_Dimensional/convert_segmented_wing_sweep.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke  

# ---------------------------------------------------------------------------------------------------------------------- 
# Imports 
# ----------------------------------------------------------------------------------------------------------------------   
import numpy as np 

# ----------------------------------------------------------------------------------------------------------------------   
#  convert_wing_sweep
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Geometry-Three_Dimensional
def convert_wing_sweep(wing,old_ref_chord_fraction = 0.0,new_ref_chord_fraction = 0.25):
    """ This method converts the sweep of a wing planform to refer to a new
    chord fraction. Defaults to converting from leading-edge sweep to 
    quarter-chord sweep.

    Assumptions:
        Assumes a simple trapezoidal wing shape. If the input wing object does
        not have a simple trapezoidal shape, this function will convert sweeps
        for an equivalent trapezoid having the same reference sweep, aspect 
        ratio, and taper ratio.
    
    Source:
        Unknown
    
    Inputs:
        wing - a data dictionary with the fields:
            apsect_ratio - wing aspect ratio                            [dimensionless]
            sweep        - wing sweep                                   [radians]
            taper        - wing taper ratio                             [dimensionless]
 
        old_ref_chord_fraction - a float value between 0 and 1.0 that 
                                 tells what fraction of the local chord
                                 the sweep line follows. (For example, 
                                 a value of 0.25 refers to quarter-chord
                                 sweep
        new_ref_chord_fraction - a float value between 0 and 1.0 that
                                 tells what fraction of the local chord
                                 is the new reference for sweep.

    Outputs:
        output - a single float value, new_sweep, which is the sweep
                 angle referenced to the new_ref_chord_fraction.

    Defaults:
        Defaults to converting from leading edge sweep to quater-chord sweep.
        
     Properties Used:
        N/A       
    """             
    # Unpack inputs
    sweep = wing.sweeps.quarter_chord
    taper = wing.taper
    if 'effective_aspect_ratio' in wing:
        ar = wing.effective_aspect_ratio
    elif 'extended' in wing:
        if 'aspect_ratio' in wing.extended:
            ar = wing.extended.aspect_ratio
        else:
            ar = wing.aspect_ratio
    else:
        ar = wing.aspect_ratio    
    
    #Convert sweep to leading edge sweep if it was not already so
    if old_ref_chord_fraction == 0.0:
        sweep_LE = wing.sweeps.leading_edge
    else:
        sweep_LE  = np.arctan(np.tan(sweep)+4*old_ref_chord_fraction*
                              (1-taper)/(ar*(1+taper)))  #Compute leading-edge sweep

    #Convert from leading edge sweep to the desired sweep reference
    new_sweep = np.arctan(np.tan(sweep_LE)-4*new_ref_chord_fraction*
                          (1-taper)/(ar*(1+taper)))  #Compute sweep referenced 
                                                     #to new chord-fraction

    return new_sweep
