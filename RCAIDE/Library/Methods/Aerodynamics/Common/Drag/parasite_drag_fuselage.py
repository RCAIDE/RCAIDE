## @ingroup Library-Methods-Aerodynamics-Common-Drag
# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/parasite_drag_fuselage.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imporst 
from RCAIDE.Framework.Core import Data
from . import compressible_turbulent_flat_plate

# python imports 
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
#   Parasite Drag Fuselage
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Aerodynamics-Common-Drag
def parasite_drag_fuselage(state,settings,fuselage):
    """Computes the parasite drag due the a fuselage (or boom)

    Assumptions:
        None

    Source:
        Stanford AA241 A/B Course Notes

    Args:
        state.conditions.freestream.
          mach_number                                (numpy.ndarray): mach_number     [Unitless]
          temperature                                (numpy.ndarray): temperature     [K]
          reynolds_number                            (numpy.ndarray): Reynolds number [Unitless]
        settings.fuselage_parasite_drag_form_factor  (numpy.ndarray): form factor     [Unitless]
        geometry.fuselage.       
          areas.front_projected                              (float): projected front area [m^2]
          areas.wetted                                       (float): wetted area          [m^2]
          lengths.total                                      (float): length               [m]
          effective_diameter                                 (float): effective diamater   [m]

    Returns:
        None 
    """

    # unpack inputs 
    freestream    = state.conditions.freestream
    Mc            = freestream.mach_number
    Tc            = freestream.temperature    
    re            = freestream.reynolds_number
    form_factor   = settings.fuselage_parasite_drag_form_factor 
    Sref          = fuselage.areas.front_projected
    Swet          = fuselage.areas.wetted 
    l_fus         = fuselage.lengths.total
    d_fus         = fuselage.effective_diameter 

    # Reynolds number
    Re_fus = re*(l_fus)
    
    # skin friction coefficient
    cf_fus, k_comp, k_reyn = compressible_turbulent_flat_plate(Re_fus,Mc,Tc)
    
    # compute form factor for cylindrical bodies
    d_d           = float(d_fus/l_fus) 
    D             = np.zeros_like(Mc)    
    D[Mc < 0.95]  = np.sqrt(1 - (1-Mc[Mc < 0.95]**2) * d_d**2)
    D[Mc >= 0.95] = np.sqrt(1 - d_d**2)

    a             = np.zeros_like(Mc)    
    a[Mc < 0.95]  = 2 * (1-Mc[Mc < 0.95]**2) * (d_d**2) *(np.arctanh(D[Mc < 0.95])-D[Mc < 0.95]) / (D[Mc < 0.95]**3)
    a[Mc >= 0.95] = 2  * (d_d**2) *(np.arctanh(D[Mc >= 0.95])-D[Mc >= 0.95]) / (D[Mc >= 0.95]**3)

    du_max_u             = np.zeros_like(Mc)    
    du_max_u[Mc < 0.95]  = a[Mc < 0.95] / ( (2-a[Mc < 0.95]) * (1-Mc[Mc < 0.95]**2)**0.5 ) 
    du_max_u[Mc >= 0.95] = a[Mc >= 0.95] / ( (2-a[Mc >= 0.95]) )
    
    k_fus                  = (1 + form_factor*du_max_u)**2 
    fuselage_parasite_drag = k_fus * cf_fus * Swet / Sref  
    
    # Store results 
    fuselage_result = Data(
        wetted_area               = Swet   , 
        reference_area            = Sref   , 
        parasite_drag             = fuselage_parasite_drag ,
        skin_friction             = cf_fus ,
        compressibility_factor    = k_comp ,
        reynolds_factor           = k_reyn , 
        form_factor               = k_fus  ,
    ) 
    state.conditions.aerodynamics.coefficients.drag.breakdown.parasite[fuselage.tag] = fuselage_result 
    
    return  