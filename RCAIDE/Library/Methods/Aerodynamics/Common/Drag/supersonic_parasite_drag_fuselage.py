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
#  Supersonic Parasite Drag Fuselage
# ---------------------------------------------------------------------------------------------------------------------- 
def supersonic_parasite_drag_fuselage(state,settings,fuselage):
    """Computes the parasite drag due to the fuselage

    Assumptions:
    Basic fit

    Source:
    http://aerodesign.stanford.edu/aircraftdesign/aircraftdesign.html (Stanford AA241 A/B Course Notes)

    Args:
    state.conditions.freestream.
      mach_number                                [Unitless]
      temperature                                [K]
      reynolds_number                            [Unitless]
    settings.fuselage_parasite_drag_form_factor  [Unitless]
    geometry.fuselage.       
      areas.front_projected                      [m^2]
      areas.wetted                               [m^2]
      lengths.total                              [m]
      effective_diameter                         [m]

    Returns:
    fuselage_parasite_drag                       [Unitless] 
    """

    # unpack inputs
    configuration = settings
    form_factor   = configuration.fuselage_parasite_drag_form_factor
    low_cutoff    = configuration.fuselage_parasite_drag_begin_blend_mach
    high_cutoff   = configuration.fuselage_parasite_drag_end_blend_mach  
    Sref          = fuselage.areas.front_projected
    Swet          = fuselage.areas.wetted 
    l_fus         = fuselage.lengths.total
    d_fus         = fuselage.effective_diameter 
    Mach          = state.conditions.freestream.mach_number
    Tc            = state.conditions.freestream.temperature    
    re            = state.conditions.freestream.reynolds_number

    # reynolds number
    Re_fus = re*(l_fus)
    
    # skin friction coefficient
    cf_fus, k_comp, k_reyn = compressible_turbulent_flat_plate(Re_fus,Mach,Tc)
    
    # form factor for cylindrical bodies
    d_d = float(d_fus)/float(l_fus)
    
    D_low        = np.zeros_like(Mach)
    a_low        = np.zeros_like(Mach)
    du_max_u_low = np.zeros_like(Mach)
    
    D_high = np.zeros_like(Mach)
    a_high = np.zeros_like(Mach)
    du_max_u_high = np.zeros_like(Mach) 
    k_fus = np.zeros_like(Mach)
    
    low_inds  = Mach < high_cutoff
    high_inds = Mach > low_cutoff
    
    D_low[low_inds]        = np.sqrt(1 - (1-Mach[low_inds]**2) * d_d**2)
    a_low[low_inds]        = 2 * (1-Mach[low_inds]**2) * (d_d**2) *(np.arctanh(D_low[low_inds])-D_low[low_inds]) / (D_low[low_inds]**3)
    du_max_u_low[low_inds] = a_low[low_inds] / ( (2-a_low[low_inds]) * (1-Mach[low_inds]**2)**0.5 )
    
    D_high[high_inds]        = np.sqrt(1 - d_d**2)
    a_high[high_inds]        = 2  * (d_d**2) *(np.arctanh(D_high[high_inds])-D_high[high_inds]) / (D_high[high_inds]**3)
    du_max_u_high[high_inds] = a_high[high_inds] / ( (2-a_high[high_inds]) )
    
    spline = Cubic_Spline_Blender(low_cutoff,high_cutoff)
    h00    = lambda M:spline.compute(M)
    
    du_max_u = du_max_u_low*(h00(Mach)) + du_max_u_high*(1-h00(Mach))    
    
    k_fus = (1 + form_factor*du_max_u)**2

    fuselage_parasite_drag = k_fus * cf_fus * Swet / Sref  
    
    # Store dat 
    results = Data(
        wetted_area               = Swet   , 
        reference_area            = Sref   , 
        total                     = fuselage_parasite_drag ,
        skin_friction             = cf_fus ,
        compressibility_factor    = k_comp ,
        reynolds_factor           = k_reyn , 
        form_factor               = k_fus  ,
    ) 
    state.conditions.aerodynamics.coefficients.drag.breakdown.parasite[fuselage.tag] = results
    return 