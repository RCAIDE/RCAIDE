# RCAIDE/Methods/Aerodynamics/Common/Drag/parasite_drag_total.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
import RCAIDE
from RCAIDE.Library.Components.Fuselages import Blended_Wing_Body_Fuselage as BWB_Fuselage
 
# package imports
import numpy as np  

# ----------------------------------------------------------------------------------------------------------------------  
#  Total Parasite Drag 
# ----------------------------------------------------------------------------------------------------------------------   
def parasite_total(state,settings,geometry):
    """Sums up the parasite drags from all compoments 

    Assumptions:
        None

    Source:
        None

    Args:
        state                                                (dict): flight conditions       [-]
        settings                                             (dict): analyses settings       [-]
        geometry                                             (dict): aircraft data stucture  [-]
        conditions.aerodynamics.coefficients.drag.
          parasite[wing.tag(s)].parasite_drag       (numpy.ndarray): wing parasite drags     [Unitless]
          parasite[fuselage.tag(s)].parasite_drag   (numpy.ndarray): fuselage parasite drags [Unitless]
          parasite[boom.tag(s)].parasite_drag       (numpy.ndarray): boom parasite drags     [Unitless]
          parasite[nacelle.tag(s)].parasite_drag    (numpy.ndarray): nacelle parasite drags  [Unitless]
          parasite[pylon.tag(s)].parasite_drag      (numpy.ndarray): pylon parasite drags    [Unitless]


    Returns:
        None 
    """

    # unpack
    conditions             = state.conditions 
    vehicle_reference_area = geometry.reference_area

    #compute parasite drag total
    total_parasite_drag = 0 *  state.state.ones_row(1)

    for wing in geometry.wings:
        total_parasite_drag +=renormalize(wing.tag, wing.areas.reference, conditions,vehicle_reference_area)

    fuselages = [f for f in geometry.fuselages if not isinstance(f, BWB_Fuselage)]
    for fuselage in fuselages:
        total_parasite_drag +=renormalize(fuselage.tag, fuselage.areas.front_projected, conditions, vehicle_reference_area)

    for network in geometry.networks:
        if 'busses' in network:
            carriers = network.busses
        if 'fuel_lines' in network:
            carriers = network.fuel_lines

        for carrier in carriers:
            nacelle_propulsors = [p for p in carrier.propulsors if 'nacelle' in p]
            for propulsor in nacelle_propulsors:
                total_parasite_drag += renormalize(propulsor.nacelle.tag,
                            propulsor.nacelle.diameter**2 / 4 * np.pi,
                            conditions,
                            vehicle_reference_area)
                if propulsor.nacelle.has_pylon:
                    total_parasite_drag += renormalize(propulsor.nacelle.tag+'_pylon',
                                propulsor.nacelle.diameter**2 / 4 * np.pi,
                                conditions,
                                vehicle_reference_area)
    
    state.conditions.aerodynamics.coefficients.drag.parasite.total = total_parasite_drag

    return 

def renormalize(tag, ref_area, conditions,vehicle_reference_area):
    p_drag = conditions.aerodynamics.coefficients.drag.parasite[tag].total
    p_drag_norm =  p_drag * ref_area/vehicle_reference_area
    conditions.aerodynamics.coefficients.drag.parasite[tag].total = p_drag_norm
    return p_drag_norm