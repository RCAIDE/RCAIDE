# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/miscellaneous_drag_aircraft.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
from RCAIDE.Framework.Core import Data

# package imports
import RNUMPY as rp

# ----------------------------------------------------------------------------------------------------------------------
#  miscellaneous_drag_aircraft
# ----------------------------------------------------------------------------------------------------------------------  
def miscellaneous_drag(state,settings,geometry):
    """Computes the miscellaneous drag associated with an aircraft

    Assumptions: 

    Source:
        ESDU 94044: Excrescence drag levels on aircraft, figure 1

    Args:
        state.conditions.freestream.mach_number          (numpy.ndarray): mach number                    [unitless]
        geometry                                                  (dict): vehicle data structure         [-] 

    Returns: 
        conditions.aerodynamics.coefficients.drag.
            .miscellaneous.total_wetted_area                      (drag): total wetted area              [unitless]  
            .miscellaneous.total                                  (drag): miscellaneous drag coefficient [unitless] 
    """


    conditions     = state.conditions  
    S_ref          = geometry.reference_area
    Mach           = conditions.freestream.mach_number 
   
    if rp.all((Mach<=1.0) == True): 
        swet_tot       = 0.
        for wing in geometry.wings:
            swet_tot += wing.areas.wetted 
        for fuselage in geometry.fuselages:
            swet_tot += fuselage.areas.wetted
        for boom in geometry.booms:
            swet_tot += boom.areas.wetted
        for network in geometry.networks: 
            if 'busses' in network:  
                for bus in network.busses:
                    for propulsor in bus.propulsors:  
                        if 'nacelle' in propulsor:
                            swet_tot += propulsor.nacelle.areas.wetted  
            if 'fuel_lines' in network:  
                for fuel_line in network.fuel_lines:
                    for propulsor in fuel_line.propulsors: 
                        if 'nacelle' in propulsor:
                            swet_tot += propulsor.nacelle.areas.wetted  
                            
        # total miscellaneous drag 
        miscellaneous_drag =  (0.40* (0.0184 + 0.000469 * swet_tot - 1.13*10**-7 * swet_tot ** 2)) / S_ref
        total_miscellaneous_drag = miscellaneous_drag *rp.ones_like(Mach)    
    else:

        # Initialize drag
        total_nacelle_base_drag   = 0.0  
        nacelle_base_drag_results = Data() 
    
        # Estimating nacelle drag 
        for network in  geometry.networks: 
            if 'busses' in network:  
                for bus in network.busses:
                    for propulsor in bus.propulsors:  
                        if 'nacelle' in propulsor: 
                            nacelle_base_drag = 0.5/12. * rp.pi * propulsor.nacelle.diameter * 0.2/S_ref 
                            nacelle_base_drag_results[propulsor.nacelle.tag] = nacelle_base_drag * rp.ones_like(Mach)   
                            total_nacelle_base_drag += nacelle_base_drag     
         
            if 'fuel_lines' in network:  
                for fuel_line in network.fuel_lines:
                    for propulsor in fuel_line.propulsors:  
                        if 'nacelle' in propulsor: 
                            nacelle_base_drag = 0.5/12. * rp.pi * propulsor.nacelle.diameter * 0.2/S_ref
                            nacelle_base_drag_results[propulsor.nacelle.tag] = nacelle_base_drag * rp.ones_like(Mach)   
                            total_nacelle_base_drag += nacelle_base_drag           
             
        #   Fuselage upsweep drag 
        fuselage_upsweep_drag = 0.006 /S_ref 
         
        # total miscellaneous drag 
        miscellaneous_drag = total_nacelle_base_drag + fuselage_upsweep_drag
        total_miscellaneous_drag = miscellaneous_drag *rp.ones_like(Mach)
        
    # Store results 
    conditions.aerodynamics.coefficients.drag.miscellaneous.total =  total_miscellaneous_drag 
    return  
