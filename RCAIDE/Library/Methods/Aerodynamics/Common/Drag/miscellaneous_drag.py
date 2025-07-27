# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/miscellaneous_drag.py 
# 
# Created:  Jun 2025, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
  
from RCAIDE.Framework.Core                    import Data  

# package imports
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
#  Miscellaneous Drag Total
# ----------------------------------------------------------------------------------------------------------------------   
def miscellaneous_drag(state,settings,geometry):
    """Computes the miscellaneous drag associated with an aircraft

    Assumptions:
    Basic fit

    Source:
    http://aerodesign.stanford.edu/aircraftdesign/aircraftdesign.html (Stanford AA241 A/B Course Notes)

    Args:
    configuration.trim_drag_correction_factor  [Unitless]
    geometry.nacelle.diameter                  [m]
    geometry.reference_area                    [m^2]
    geometry.wings['main_wing'].aspect_ratio   [Unitless]
    state.conditions.freestream.mach_number    [Unitless] (actual values are not used)

    Returns:
    total_miscellaneous_drag                   [Unitless] 
    """ 

    conditions     = state.conditions  
    S_ref          = geometry.reference_area
    Mach           = conditions.freestream.mach_number 
   
    # landing gear drag  
    landing_gear_drag  =  np.zeros_like(Mach)
    for landing_gear in  geometry.landing_gears:
        if landing_gear.gear_extended == True:
            if landing_gear.fairing:
                cd_lg = 0.15
            else:
                cd_lg = 0.30
            landing_gear_drag[:,0] +=  landing_gear.wheels *  cd_lg * (landing_gear.tire_diameter * landing_gear.tire_width) /S_ref 
         
    # miscellaneous drag
    miscellaneous_drag =  np.zeros_like(Mach)
    if np.all((Mach<=1.0) == True):  # Subsonic
        swet_tot       = 0.
        for wing in geometry.wings:
            swet_tot += wing.areas.wetted 
        for fuselage in geometry.fuselages:
            swet_tot += fuselage.areas.wetted
        for boom in geometry.booms:
            swet_tot += boom.areas.wetted
        for network in geometry.networks: 
            for propulsor in network.propulsors:  
                if 'nacelle' in propulsor: 
                    if propulsor.nacelle !=  None:                    
                        swet_tot += propulsor.nacelle.areas.wetted
                            
        # Total miscellaneous drag 
        miscellaneous_drag[:,0] =  (0.40* (0.0184 + 0.000469 * swet_tot - 1.13*10**-7 * swet_tot ** 2)) / S_ref    
    else:  
        # Initialize drag
        total_nacelle_base_drag   = 0.0   
        # Estimating nacelle drag 
        for network in  geometry.networks: 
            for propulsor in network.propulsors:  
                if 'nacelle' in propulsor: 
                    if propulsor.nacelle !=  None:                    
                        nacelle_base_drag = 0.5/12. * np.pi * propulsor.nacelle.diameter * 0.2/S_ref  
                        total_nacelle_base_drag += nacelle_base_drag     

        # Fuselage upsweep drag 
        fuselage_upsweep_drag = 0.006 /S_ref  
        miscellaneous_drag[:,0] = total_nacelle_base_drag + fuselage_upsweep_drag
        
    total_miscellaneous_drag = miscellaneous_drag + landing_gear_drag
        
    # Store results 
    conditions.aerodynamics.coefficients.drag.miscellaneous = Data(  total  = total_miscellaneous_drag)
    return  
    
