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
#  convert_segmented_wing_sweep
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Library-Methods-Geometry-Three_Dimensional
def convert_segmented_wing_sweep(old_sweep, seg_a, seg_b, wing, old_ref_chord_fraction=0.0, new_ref_chord_fraction=0.25):
    """ This method converts the sweep of a section of a wing between two segments 
    to refer to a new chord fraction. More specifically, it converts the inboard 
    segment's (seg_a's) outboard sweep. Defaults to converting from leading-edge sweep to 
    quarter-chord sweep.

    Assumptions:
        Assumes a simple trapezoidal section shape. If the input section does
        not have a simple trapezoidal shape, this function will convert sweeps
        for an equivalent trapezoid having the same reference sweep, aspect 
        ratio, and taper ratio.
    
    Source:
        Unknown
    
    Inputs:
        old_sweep - sweep angle to convert
    
        seg_a and seg_b - two Segment() objects with:
            root_chord_percent    - percent of the wing's root chord
    
        wing - a data dictionary with the fields:
            chords.root  - root chord                              [m]
            span         - wingspan                                [m]
            symmetric    - symmetry                                [boolean]
 
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
    if old_ref_chord_fraction==new_ref_chord_fraction:
        return old_sweep
    
    # Unpack inputs    
    sweep          = old_sweep
    
    root_chord     = seg_a.root_chord_percent *wing.chords.root
    tip_chord      = seg_b.root_chord_percent *wing.chords.root
    taper          = tip_chord / root_chord
    
    wingspan       = wing.spans.projected if wing.symmetric else wing.spans.projected *2 #calculation is for full wingspan
    section_span   = wingspan *(seg_b.percent_span_location - seg_a.percent_span_location)
    chord_mean_geo = 0.5 * (root_chord + tip_chord)
    ar             = section_span / chord_mean_geo  
    
    #Convert sweep to leading edge sweep if it was not already so
    if old_ref_chord_fraction == 0.0:
        sweep_LE = old_sweep
    else:
        sweep_LE  = np.arctan(np.tan(sweep)+4*old_ref_chord_fraction*
                              (1-taper)/(ar*(1+taper)))  #Compute leading-edge sweep

    #Convert from leading edge sweep to the desired sweep reference
    new_sweep = np.arctan(np.tan(sweep_LE)-4*new_ref_chord_fraction*
                          (1-taper)/(ar*(1+taper)))  #Compute sweep referenced 
                                                     #to new chord-fraction

    return new_sweep



def _convert_segmented_wing_sweep(State, Settings, System):
	'''
	Framework version of convert_segmented_wing_sweep.
	Wraps convert_segmented_wing_sweep with State, Settings, System pack/unpack.
	Please see convert_segmented_wing_sweep documentation for more details.
	'''

	#TODO: old_sweep              = [Replace With State, Settings, or System Attribute]
	#TODO: seg_a                  = [Replace With State, Settings, or System Attribute]
	#TODO: seg_b                  = [Replace With State, Settings, or System Attribute]
	#TODO: wing                   = [Replace With State, Settings, or System Attribute]
	#TODO: old_ref_chord_fraction = [Replace With State, Settings, or System Attribute]
	#TODO: new_ref_chord_fraction = [Replace With State, Settings, or System Attribute]

	results = convert_segmented_wing_sweep('old_sweep', 'seg_a', 'seg_b', 'wing', 'old_ref_chord_fraction', 'new_ref_chord_fraction')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System