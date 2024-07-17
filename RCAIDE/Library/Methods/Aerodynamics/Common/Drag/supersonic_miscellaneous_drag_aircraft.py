# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/supersonic_miscellaneous_drag_aircraft.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
  
from RCAIDE.Framework.Core                    import Data  

# package imports
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
#  Supersonic Miscellaneous Drag Total
# ----------------------------------------------------------------------------------------------------------------------   
def supersonic_miscellaneous_drag_aircraft(state,settings,geometry):
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
     
    vehicle_reference_area = geometry.reference_area
    conditions             = state.conditions 
    
    # Initialize drag
    total_nacelle_base_drag   = 0.0
    total_gap_drag            = 0.0 
    nacelle_base_drag_results = Data() 

    # Estimating nacelle drag 
    for network in  geometry.networks: 
        if 'busses' in network:  
            for bus in network.busses:
                for propulsor in bus.propulsors:  
                    if 'nacelle' in propulsor: 
                        nacelle_base_drag = 0.5/12. * np.pi * propulsor.nacelle.diameter * 0.2/vehicle_reference_area 
                        nacelle_base_drag_results[propulsor.nacelle.tag] = nacelle_base_drag * state.ones_row(1)  
                        total_nacelle_base_drag += nacelle_base_drag     
     
        if 'fuel_lines' in network:  
            for fuel_line in network.fuel_lines:
                for propulsor in fuel_line.propulsors:  
                    if 'nacelle' in propulsor: 
                        nacelle_base_drag = 0.5/12. * np.pi * propulsor.nacelle.diameter * 0.2/vehicle_reference_area 
                        nacelle_base_drag_results[propulsor.nacelle.tag] = nacelle_base_drag * state.ones_row(1)  
                        total_nacelle_base_drag += nacelle_base_drag           
         
    #   Fuselage upsweep drag 
    fuselage_upsweep_drag = 0.006 / vehicle_reference_area
     
    #   Fuselage base drag 
    fuselage_base_drag = 0.0
     
    # total miscellaneousdrag 
    total_miscellaneous_drag = total_gap_drag  + total_nacelle_base_drag + fuselage_upsweep_drag  + fuselage_base_drag  
    
    # dump to results
    conditions.aerodynamics.coefficients.drag.breakdown.miscellaneous = Data(
        fuselage_upsweep = fuselage_upsweep_drag     *state.ones_row(1)  , 
        nacelle_base     = nacelle_base_drag_results ,
        fuselage_base    = fuselage_base_drag        *state.ones_row(1)  ,
        control_gaps     = total_gap_drag            *state.ones_row(1)  ,
        total            = total_miscellaneous_drag  *state.ones_row(1)  ,
    )
       
    return  
    
