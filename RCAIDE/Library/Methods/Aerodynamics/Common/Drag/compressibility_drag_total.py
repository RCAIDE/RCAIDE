# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/compressibility_drag_total.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
  
from RCAIDE.Framework.Core                    import Data 
from RCAIDE.Library.Components.Wings          import Main_Wing
from RCAIDE.Library.Methods.Utilities         import Cubic_Spline_Blender  
from .supersonic_wave_drag_lift               import supersonic_wave_drag_lift
from .supersonic_wave_drag_volume_raymer      import supersonic_wave_drag_volume_raymer
from .supersonic_wave_drag_volume_sears_haack import supersonic_wave_drag_volume_sears_haack

# package imports
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
#  Supersonic Compressibility Drag Total
# ----------------------------------------------------------------------------------------------------------------------  
def compressibility_drag_total(state,settings,geometry):
    """Computes compressibility drag for full aircraft including volume drag

    Assumptions:
    None

    Source:
    None

    Args:   
    settings.
      begin_drag_rise_mach_number                                    [Unitless]
      end_drag_rise_mach_number                                      [Unitless]
      peak_mach_number                                               [Unitless]
      transonic_drag_multiplier                                      [Unitless]
      volume_wave_drag_scaling                                       [Unitless]
    state.conditions.aerodynamics.lift_breakdown.compressible_wings  [Unitless]
    state.conditions.freestream.mach_number                          [Unitless]
    geometry.maximum_cross_sectional_area                            [m^2] (used in subfunctions)
    geometry.total_length                                            [m]   (used in subfunctions)
    geometry.reference_area                                          [m^2]
    geometry.wings                             

    Returns:
    total_compressibility_drag                                       [Unitless]

    Properties Used:
    None
    """     

    # Unpack
    conditions  = state.conditions
    Mach        = conditions.freestream.mach_number 
    Cl_wings    = conditions.aerodynamics.coefficients.lift.compressible_wings 
    S_ref       = geometry.reference_area       
     
    if np.all((Mach<=1.0) == True):  
        # intiialize parasite drag total
        total_compressibility_drag = 0.0
        
        # loop through wings 
        for wing in geometry.wings:
            s_wing = wing.areas.reference
            compressibility_drag = state.conditions.aerodynamics.coefficients.drag.compressible[wing.tag].total
            state.conditions.aerodynamics.coefficients.drag.compressible[wing.tag].total = compressibility_drag * 1. # avoid linking variables
            total_compressibility_drag += compressibility_drag * (s_wing/S_ref)
    
        state.conditions.aerodynamics.coefficients.drag.compressible.total  = total_compressibility_drag
    else: 
        # supersonic 
        low_mach_cutoff  = settings.supersonic.begin_drag_rise_mach_number
        high_mach_cutoff = settings.supersonic.end_drag_rise_mach_number
        peak_mach        = settings.supersonic.peak_mach_number
        peak_factor      = settings.supersonic.transonic_drag_multiplier
        scaling_factor   = settings.supersonic.volume_wave_drag_scaling
        
        if settings.supersonic.wave_drag_type == 'Raymer':
            wave_drag_volume = supersonic_wave_drag_volume_raymer
        elif settings.supersonic.wave_drag_type == 'Sears-Haack':
            wave_drag_volume = supersonic_wave_drag_volume_sears_haack
        else:
            raise NotImplementedError    
        
        if settings.supersonic.cross_sectional_area_calculation_type != 'Fixed':
            raise NotImplementedError
    
        low_cutoff_volume_total  = np.zeros_like(Mach)
        high_cutoff_volume_total = np.zeros_like(Mach)    
        for wing in geometry.wings:
            low_cutoff_volume_total += drag_div(low_mach_cutoff*np.ones([1]), wing, Cl_wings[wing.tag], S_ref)[0]
        high_cutoff_volume_total = wave_drag_volume(geometry,low_mach_cutoff*np.ones([1]),scaling_factor)
        
        peak_volume_total = high_cutoff_volume_total*peak_factor
         
        # subsonic side
        a1 = (low_cutoff_volume_total-peak_volume_total)/(low_mach_cutoff-peak_mach)/(low_mach_cutoff-peak_mach)
        
        # supersonic side
        a2 = (high_cutoff_volume_total-peak_volume_total)/(high_mach_cutoff-peak_mach)/(high_mach_cutoff-peak_mach) 
        
        # Shorten cubic Hermite spline
        sub_spline = Cubic_Spline_Blender(low_mach_cutoff, peak_mach-(peak_mach-low_mach_cutoff)*3/4)
        sup_spline = Cubic_Spline_Blender(peak_mach,high_mach_cutoff)
        sub_h00    = lambda M:sub_spline.compute(M)
        sup_h00    = lambda M:sup_spline.compute(M)
        
        
        low_inds = Mach[:,0]<peak_mach
        hi_inds  = Mach[:,0]>=peak_mach
    
        cd_c_v_base = np.zeros_like(Mach)
        cd_c_l_base = np.zeros_like(Mach)
        for wing in geometry.wings:
            cd_c_v_base[low_inds] += drag_div(Mach[low_inds], wing, Cl_wings[wing.tag][low_inds],S_ref)[0]
            cd_c_l_base += lift_wave_drag(conditions, settings, wing, S_ref)
        cd_c_v_base[Mach>=peak_mach] = wave_drag_volume(geometry, Mach[Mach>=peak_mach], scaling_factor) 
        
        cd_c_v = np.zeros_like(Mach)
        
        cd_c_v[low_inds] = cd_c_v_base[low_inds]*(sub_h00(Mach[low_inds])) + transonic_drag_function(Mach[low_inds],a1[low_inds], peak_mach, peak_volume_total)*(1-sub_h00(Mach[low_inds]))
        cd_c_v[hi_inds]  = transonic_drag_function(Mach[hi_inds],a2, peak_mach, peak_volume_total)*(sup_h00(Mach[hi_inds])) + cd_c_v_base[hi_inds]*(1-sup_h00(Mach[hi_inds]))
    
        if peak_mach<1.01:
            print('Warning: a peak Mach number of less than 1.01 will cause a small discontinuity in lift wave drag')
        cd_c_l = cd_c_l_base*(1-sup_h00(Mach))
        
        cd_c = cd_c_v + cd_c_l 
        
        # Save drag breakdown 
        drag = conditions.aerodynamics.coefficients.drag.compressible.total   = cd_c
        
    return  

# ---------------------------------------------------------------------------------------------------------------------- 
#  transonic_drag_function
# ---------------------------------------------------------------------------------------------------------------------- 
def transonic_drag_function(Mach,a_vertex, peak_mach, peak_volume_total):
    """  parabolic approximation of drag rise in the transonic region
    
    Assumptions:
    Basic fit

    Source:
    None 

    Args:
    Mach
    a_vertex
    peak_mach
    peak_volume_total

    Returns:
    transonic_drag
    """ 
    transonic_drag = a_vertex*(Mach-peak_mach)*(Mach-peak_mach)+peak_volume_total
    transonic_drag = transonic_drag.reshape(np.shape(Mach))
    return transonic_drag

# ---------------------------------------------------------------------------------------------------------------------- 
# lift_wave_drag
# ---------------------------------------------------------------------------------------------------------------------- 
def lift_wave_drag(conditions,configuration,wing,Sref_main):
    """Determine lift wave drag for supersonic speeds

    Assumptions:
    Basic fit

    Source:
    http://aerodesign.stanford.edu/aircraftdesign/aircraftdesign.html (Stanford AA241 A/B Course Notes)

    Args:
    conditions.freestream.mach_number [-]
    configuration                     (passed to another function)
    wing.areas.reference              [m^2]
    Sref_main                         [m^2] Main reference area

    Returns:
    cd_c_l                            [-] Wave drag CD due to lift 
    """        
    # Unpack Mach number
    Mach       = conditions.freestream.mach_number

    # Initalize cd arrays
    cd_c_l = np.zeros_like(Mach) 

    # Calculate wing values at all Mach numbers
    cd_lift_wave = supersonic_wave_drag_lift(conditions,configuration,wing)

    # Pack supersonic results into correct elements
    cd_c_l[Mach >= 1.01] = cd_lift_wave[0:len(Mach[Mach >= 1.01]),0]

    # Convert coefficient to full aircraft value
    cd_c_l = cd_c_l*wing.areas.reference/Sref_main

    return cd_c_l

# ----------------------------------------------------------------------------------------------------------------------
# drag_div
# ----------------------------------------------------------------------------------------------------------------------
def drag_div(Mach_ii,wing,Cl_wings,Sref_main):
    """Use drag divergence Mach number to determine drag for subsonic speeds

    Assumptions:
    Basic fit, subsonic

    Source:
    http://aerodesign.stanford.edu/aircraftdesign/aircraftdesign.html (Stanford AA241 A/B Course Notes)
    Concorde data can be found in "Supersonic drag reduction technology in the scaled supersonic 
    experimental airplane project by JAXA" by Kenji Yoshida

    Args:
    wing.
      thickness_to_chord    [-]     
      sweeps.quarter_chord  [radians]
      high_mach             [Boolean]
      areas.reference       [m^2]

    Returns:
    cd_c                    [-]
    Machc                   [-]
    MDiv                    [-]
 
    """           
    # Check if the wing is designed for high subsonic cruise
    # If so use arbitrary divergence point as correlation will not work
    if wing.high_mach is True: 
        # Divergence Mach number, fit to Concorde data
        MDiv   =  0.98 * np.ones_like(Mach_ii) 
        Machc  =  0.95 * np.ones_like(Mach_ii)  
    else:
        # Unpack wing
        t_c_w   = wing.thickness_to_chord
        sweep_w = wing.sweeps.quarter_chord

        # Check if this is the main wing, other wings are assumed to have no lift
        if isinstance(wing, Main_Wing):
            Cl_wings_w = Cl_wings
        else:
            Cl_wings_w = 0

        # Get effective Cl_wings and sweep
        cos_sweep = np.cos(sweep_w)
        tc = t_c_w / cos_sweep
        Cl_wings = Cl_wings_w / (cos_sweep*cos_sweep)

        # Compressibility drag based on regressed fits from AA241
        Machc_cos_ws = 0.922321524499352  - 1.153885166170620*tc - 0.304541067183461*Cl_wings + 0.332881324404729*tc*tc \
                    + 0.467317361111105*tc*Cl_wings + 0.087490431201549*Cl_wings*Cl_wings

        # Crest-critical Mach number, corrected for wing sweep
        Machc = Machc_cos_ws / cos_sweep

        # Divergence Mach number
        MDiv = Machc * ( 1.02 + 0.08*(1 - cos_sweep) )        

    # Divergence ratio
    mo_Mach = Mach_ii/Machc

    # Compressibility correlation, Shevell
    dcdc_cos3g = 0.0019*mo_Mach**14.641

    # Compressibility drag 
    # Sweep correlation cannot be used if the wing has a high Mach design
    if wing.high_mach is True:
        cd_c = dcdc_cos3g
    else:
        cd_c = dcdc_cos3g * (np.cos(sweep_w))**3
        
    cd_c = cd_c*wing.areas.reference/Sref_main    
    
    # Change empty format to avoid errors in assignment of returned values
    if np.shape(cd_c) == (0,0):
        cd_c = np.reshape(cd_c,[0,1]) 
        Machc  = np.reshape(Machc,[0,1]) 
        MDiv = np.reshape(MDiv,[0,1]) 

    return (cd_c,Machc,MDiv)
