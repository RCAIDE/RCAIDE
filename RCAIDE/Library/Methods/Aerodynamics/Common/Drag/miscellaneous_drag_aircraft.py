## @ingroup Library-Methods-Aerodynamics-Common-Drag
# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/miscellaneous_drag_aircraft.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
from RCAIDE.Framework.Core import Data

# package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  miscellaneous_drag_aircraft
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Methods-Aerdoynamics-Common-Drag
def miscellaneous_drag_aircraft(state,settings,geometry):
    """Computes the miscellaneous drag associated with an aircraft

    Assumptions: 

    Source:
        ESDU 94044: Excrescence drag levels on aircraft, figure 1

    Args:
        state.conditions.freestream.mach_number          (numpy.ndarray): mach number                    [unitless]
        geometry                                                  (dict): vehicle data structure         [-] 

    Returns: 
        conditions.aerodynamics.coefficients.drag.breakdown.
            .miscellaneous.total_wetted_area                      (drag): total wetted area              [unitless]  
            .miscellaneous.total                                  (drag): miscellaneous drag coefficient [unitless] 
    """

    # unpack inputs 
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
