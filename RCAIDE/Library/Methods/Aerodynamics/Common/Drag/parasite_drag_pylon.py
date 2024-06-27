## @ingroup Library-Methods-Aerodynamics-Common-Drag
# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/pparasite_drag_pylon.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
# RCAIDE imporst 
from RCAIDE.Framework.Core import Data 

# python imports 
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
#  Pylon Drag Fuselage
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Aerodynamics-Common-Drag  
def parasite_drag_pylon(state,settings,geometry):
    """Computes the parasite drag due to pylons as a proportion of the network 

    Assumptions:
        None 

    Source:
        Stanford AA241 A/B Course Notes

    Args:
        state.conditions.aerodynamics.coefficients.drag.breakdown.parasite[network.tag].
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
    
    drag          = state.conditions.aerodynamics.coefficients.drag.breakdown
    pylon_factor  = 0.2  

    # Estimating pylon drag
    for network in  geometry.networks: 
        if 'busses' in network:  
            for bus in network.busses:
                for propulsor in bus.propulsors:  
                    if 'nacelle' in propulsor:
                        nacelle              =  propulsor.nacelle
                        if nacelle.has_pylon:
                            ref_area             = nacelle.diameter**2 / 4 * np.pi
                            pylon_parasite_drag  = pylon_factor *  drag.parasite[nacelle.tag].parasite_drag* (ref_area/geometry.reference_area)
                            pylon_wetted_area    = pylon_factor *  drag.parasite[nacelle.tag].wetted_area  
                            pylon_cf             = drag.parasite[nacelle.tag].skin_friction 
                            pylon_compr_fact     = drag.parasite[nacelle.tag].compressibility_factor
                            pylon_rey_fact       = drag.parasite[nacelle.tag].reynolds_factor
                            pylon_FF             = drag.parasite[nacelle.tag].form_factor 
                            pylon_result         = Data(
                                wetted_area               = pylon_wetted_area   ,
                                reference_area            = geometry.reference_area   ,
                                parasite_drag             = pylon_parasite_drag ,
                                skin_friction             = pylon_cf  ,
                                compressibility_factor    = pylon_compr_fact   ,
                                reynolds_factor           = pylon_rey_fact   ,
                                form_factor               = pylon_FF   , )
                            drag.parasite[ nacelle.tag + '_pylon'] = pylon_result
                        else:
                            pylon_result = Data(
                                wetted_area               = 0 ,
                                reference_area            = geometry.reference_area  ,
                                parasite_drag             = np.zeros_like(drag.parasite[nacelle.tag].skin_friction)  ,
                                skin_friction             = 0 ,
                                compressibility_factor    = 0 ,
                                reynolds_factor           = 0 ,
                                form_factor               = 0 , )
                            drag.parasite[ nacelle.tag + '_pylon'] = pylon_result
     
        if 'fuel_lines' in network:  
            for fuel_line in network.fuel_lines:
                for propulsor in fuel_line.propulsors:  
                    if 'nacelle' in propulsor:
                        nacelle              = propulsor.nacelle
                        if nacelle.has_pylon:
                            ref_area             = nacelle.diameter**2 / 4 * np.pi
                            pylon_parasite_drag  = pylon_factor *  drag.parasite[nacelle.tag].parasite_drag* (ref_area/geometry.reference_area)
                            pylon_wetted_area    = pylon_factor *  drag.parasite[nacelle.tag].wetted_area  
                            pylon_cf             = drag.parasite[nacelle.tag].skin_friction 
                            pylon_compr_fact     = drag.parasite[nacelle.tag].compressibility_factor
                            pylon_rey_fact       = drag.parasite[nacelle.tag].reynolds_factor
                            pylon_FF             = drag.parasite[nacelle.tag].form_factor  
                            pylon_result = Data(
                                wetted_area               = pylon_wetted_area   ,
                                reference_area            = geometry.reference_area   ,
                                parasite_drag             = pylon_parasite_drag ,
                                skin_friction             = pylon_cf  ,
                                compressibility_factor    = pylon_compr_fact   ,
                                reynolds_factor           = pylon_rey_fact   ,
                                form_factor               = pylon_FF   , )
                            drag.parasite[ nacelle.tag + '_pylon'] = pylon_result
                        else:
                            pylon_result = Data(
                                wetted_area               = 0 ,
                                reference_area            = geometry.reference_area  ,
                                parasite_drag             = np.zeros_like(drag.parasite[nacelle.tag].skin_friction)  ,
                                skin_friction             = 0 ,
                                compressibility_factor    = 0 ,
                                reynolds_factor           = 0 ,
                                form_factor               = 0 , )
                            drag.parasite[ nacelle.tag + '_pylon'] = pylon_result
 
    return 