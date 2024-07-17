## @ingroup Methods-Aerodynamics-Common-Drag
# RCAIDE/Methods/Aerodynamics/Common/Drag/miscellaneous_drag_aircraft.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
import  numpy as  np 
from RCAIDE.Framework.Core import Data  

# ----------------------------------------------------------------------------------------------------------------------
#  miscellaneous_drag_aircraft
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Methods-Aerodynamics-Common-Drag
def miscellaneous_drag_aircraft(state,settings,geometry):
    """Computes the miscellaneous drag associated with an aircraft

    Assumptions:
    Basic fit

    Source:
    ESDU 94044, figure 1

    Args:
    state.conditions.freestream.mach_number    [Unitless] (actual values not used)
    geometry.reference_area                    [m^2]
    geometry.wings.areas.wetted                [m^2]
    geometry.fuselages.areas.wetted            [m^2]
    geometry.network.areas.wetted              [m^2]
    geometry.network.number_of_engines         [Unitless]

    Returns:
    cd_excrescence (drag)                      [Unitless]

    Properties Used:
    N/A
    """ # unpack inputs 
    conditions     = state.conditions  
    S_ref          = geometry.reference_area 

    # Estimating total wetted area
    swet_tot        = 0.
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
    swet_tot *= 1.10

    # estimate excrescence drag, based in ESDU 94044 
    cd_excrescence      = np.zeros_like(conditions.freestream.mach_number)
    cd_excrescence[:,0] = (0.40* (0.0184 + 0.000469 * swet_tot - 1.13*10**-7 * swet_tot ** 2)) / S_ref
 
    # store results 
    conditions.aerodynamics.coefficients.drag.breakdown.miscellaneous = Data(
        total_wetted_area         = swet_tot, 
        total                     = cd_excrescence)

    return  
