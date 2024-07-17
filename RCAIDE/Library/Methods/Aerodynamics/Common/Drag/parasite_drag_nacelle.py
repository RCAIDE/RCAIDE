# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/parasite_drag_nacelle.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imporst 
from RCAIDE.Framework.Core import Data
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Helper_Functions import compressible_turbulent_flat_plate

# python imports 
import numpy as np 

# ---------------------------------------------------------------------------------------------------------------------- 
#   Parasite Drag Nacelle
# ---------------------------------------------------------------------------------------------------------------------- 
def parasite_drag_nacelle(state,settings,geometry):
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
                        nacelle_drag(state,propulsor.nacelle)
     
        if 'fuel_lines' in network:  
            for fuel_line in network.fuel_lines:
                for propulsor in fuel_line.propulsors:  
                    if 'nacelle' in propulsor:
                        nacelle_drag(state,propulsor.nacelle)
                        
    return    


# ---------------------------------------------------------------------------------------------------------------------- 
#  Nacelle Drag 
# ---------------------------------------------------------------------------------------------------------------------- 
def nacelle_drag(state, nacelle):
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
     
    conditions = state.conditions 
    freestream = conditions.freestream
    Mc         = freestream.mach_number
    Tc         = freestream.temperature    
    Re         = freestream.reynolds_number
    Sref       = nacelle.diameter**2. / 4. * np.pi
    Swet       = nacelle.areas.wetted 

    # Reynolds number
    Re_prop = Re*nacelle.length
    
    # Skin friction coefficient
    cf_prop, k_comp, k_reyn = compressible_turbulent_flat_plate(Re_prop,Mc,Tc)
    
    # Form factor according to Raymer equation
    k_prop = 1 + 0.35 / ( nacelle.length/nacelle.diameter)   
   
    # find the final result    
    parasite_drag = k_prop * cf_prop * Swet / Sref
    
    # Store Data 
    propulsor_result = Data(
        wetted_area               = Swet    , 
        reference_area            = Sref    , 
        total                     = parasite_drag,
        skin_friction             = cf_prop ,
        compressibility_factor    = k_comp  ,
        reynolds_factor           = k_reyn  , 
        form_factor               = k_prop  ,
    ) 
    conditions.aerodynamics.coefficients.drag.breakdown.parasite[nacelle.tag] = propulsor_result
    
    return   