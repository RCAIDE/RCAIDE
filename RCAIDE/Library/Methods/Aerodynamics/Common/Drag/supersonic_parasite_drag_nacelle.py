# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/supersonic_parasite_drag_fuselage.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
  
from RCAIDE.Framework.Core                    import Data  
from RCAIDE.Library.Methods.Utilities         import Cubic_Spline_Blender   
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Helper_Functions import compressible_turbulent_flat_plate

# package imports
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
#  Supersonic Parasite Drag Nacekke 
# ---------------------------------------------------------------------------------------------------------------------- 
def supersonic_parasite_drag_nacelle(state,settings,geometry):
    """Computes the parasite drag due to the nacelle

    Assumptions:
        None 

    Source:
        None 

    Args: 
        state.conditions.freestream.mach_number      (numpy.ndarray): mach_number      [Unitless]
        state.conditions.freestream.temperature      (numpy.ndarray): temperature      [K]
        state.conditions.freestream.reynolds_number  (numpy.ndarray): Reynolds number  [Unitless]
        settings                                              (dict): analyses settings [-]
        geometry                                              (dict): aircraft geometry [-]

    Returns:
        None 
    """
     
    # Estimating nacelle drag 
    for network in  geometry.networks: 
        if 'busses' in network:  
            for bus in network.busses:
                for propulsor in bus.propulsors:  
                    if 'nacelle' in propulsor: 
                        nacelle_drag(state,settings,propulsor.nacelle)
     
        if 'fuel_lines' in network:  
            for fuel_line in network.fuel_lines:
                for propulsor in fuel_line.propulsors:  
                    if 'nacelle' in propulsor:
                        nacelle_drag(state,settings,propulsor.nacelle)
                        
    return     
# ---------------------------------------------------------------------------------------------------------------------- 
#  Nacelle Drag 
# ---------------------------------------------------------------------------------------------------------------------- 
def nacelle_drag(state,settings, nacelle):
    """helperr fuction to computes the parasite drag due to the nacelle

    Assumptions:
        None 

    Source:
        Stanford AA241 A/B Course Notes

    Args: 
        state.conditions.freestream.mach_number      (numpy.ndarray): mach_number      [Unitless]
        state.conditions.freestream.temperature      (numpy.ndarray): temperature      [K]
        state.conditions.freestream.reynolds_number  (numpy.ndarray): Reynolds number  [Unitless]
        settings                                              (dict): analyses settings [-] 

    Returns:
        None 
    """

    # unpack inputs
    conditions       = state.conditions
    freestream       = conditions.freestream
    Mach             = freestream.mach_number
    Tc               = freestream.temperature    
    re               = freestream.reynolds_number 
    low_mach_cutoff  = settings.begin_drag_rise_mach_number
    high_mach_cutoff = settings.end_drag_rise_mach_number 
    Sref             = nacelle.diameter**2 / 4 * np.pi
    Swet             = nacelle.areas.wetted 
    l_prop           = nacelle.length
    d_prop           = nacelle.diameter 

    # reynolds number
    Re_prop = re*l_prop
    
    # skin friction coefficient
    cf_prop, k_comp, k_reyn = compressible_turbulent_flat_plate(Re_prop,Mach,Tc) 
    
    # form factor according to Raymer equation (pg 283 of Aircraft Design: A Conceptual Approach)
    k_prop_sub = 1. + 0.35 / (float(l_prop)/float(d_prop)) 
    
    # for supersonic flow (http://adg.stanford.edu/aa241/drag/BODYFORMFACTOR.HTML)
    k_prop_sup = 1.
    
    trans_spline = Cubic_Spline_Blender(low_mach_cutoff,high_mach_cutoff)
    h00 = lambda M:trans_spline.compute(M)
    
    k_prop = k_prop_sub*(h00(Mach)) + k_prop_sup*(1-h00(Mach))
     
    # find the final result    
    nacelle_parasite_drag = k_prop * cf_prop * Swet / Sref   
    
    # store results
    results = Data(
        wetted_area               = Swet    , 
        reference_area            = Sref    , 
        total                     = nacelle_parasite_drag ,
        skin_friction             = cf_prop ,
        compressibility_factor    = k_comp  ,
        reynolds_factor           = k_reyn  , 
        form_factor               = k_prop  ,
    )
    state.conditions.aerodynamics.coefficients.drag.breakdown.parasite[nacelle.tag] = results    
    
    return
 