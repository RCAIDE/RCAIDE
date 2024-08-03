# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/pparasite_drag_pylon.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imports
from RCAIDE.Reference.Core import Data

# python imports 
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
#  Pylon Drag Fuselage
# ----------------------------------------------------------------------------------------------------------------------   
def parasite_drag_pylon(state,settings,geometry):
    """Computes the parasite drag due to pylons as a proportion of the network 

    Assumptions:
        None 

    Source:
        Stanford AA241 A/B Course Notes

    Args:
        state.conditions.aerodynamics.coefficients.drag.parasite[network.tag].
          form_factor                      (float): form_factor              [Unitless]
          compressibility_factor           (float): compressibility_factor   [Unitless]
          skin_friction            (numpy.ndarray): skin_friction            [Unitless]
          wetted_area              (numpy.ndarray): wetted_area              [m^2]
          parasite_drag            (numpy.ndarray): parasite_drag            [Unitless]
          reynolds_number          (numpy.ndarray): reynolds_number          [Unitless]
        geometry                            (dict): aircraft geometry        [-]

    Returns:
        None 
    """
    
    drag          = state.conditions.aerodynamics.coefficients.drag
    pylon_factor  = 0.2

    # Estimating pylon drag
    for network in  geometry.networks: 
        if 'busses' in network:
            carriers = network.busses
        if 'fuel_lines' in network:
            carriers = network.fuel_lines

        for carrier in carriers:
            nacelle_propulsors = [p for p in carrier.propulsors if 'nacelle' in p]
            for propulsor in nacelle_propulsors:
                nacelle = propulsor.nacelle
                pylon = nacelle.has_pylon
                pylon_result         = Data(
                    wetted_area            =(0
                                             + pylon * pylon_factor * drag.parasite[nacelle.tag].wetted_area),
                    reference_area         =geometry.reference_area,

                    skin_friction          =(0
                                             + pylon * drag.parasite[nacelle.tag].skin_friction),
                    compressibility_factor =(0
                                             + pylon * drag.parasite[nacelle.tag].compressibility_factor),
                    reynolds_factor        =(0
                                             + pylon * drag.parasite[nacelle.tag].reynolds_factor),
                    form_factor            =(0
                                                + pylon * drag.parasite[nacelle.tag].form_factor),
                    total                  =(np.zeros_like(drag.parasite[nacelle.tag].skin_friction)
                                             + pylon * pylon_factor * drag.parasite[nacelle.tag].total
                                             * (nacelle.diameter ** 2 / 4 * np.pi / geometry.reference_area))
                )
                drag.parasite[nacelle.tag + '_pylon'] = pylon_result

    return
