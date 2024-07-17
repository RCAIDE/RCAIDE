# RCAIDE/Methods/Aerodynamics/Common/Drag/compressibility_drag_wing_total.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 
 
# ----------------------------------------------------------------------------------------------------------------------  
#   Compressibility Drag for Wings 
# ----------------------------------------------------------------------------------------------------------------------    
def compressibility_drag_wing_total(state,settings,geometry):
    """Sums compressibility drag for all wings  

    Assumptions:
        None

    Source:
        Stanford AA241 A/B Course Notes

    Args:
        state.conditions.aerodynamics.coefficients.drag.breakdown.
            compressible[wing.tag].compressibility_drag (numpy.ndarray): compressibility drag of individual wings  [Unitless]
        settings                                                 (dict): analyses settings                         [-]
        geometry.wings.areas.reference                          (float): area of wings                             [m^2]
        geometry.reference_area                                 (float): reference area of aircraft                [m^2]
        

    Returns:
        total_compressibility_drag (numpy.ndarray): total compressibility drag  [Unitless] 
    """  
    # unpack 
    S_ref                  = geometry.reference_area 
    
    # intiialize parasite drag total
    total_compressibility_drag = 0.0
    
    # loop through wings 
    for wing in geometry.wings:
        s_wing = wing.areas.reference
        compressibility_drag = state.conditions.aerodynamics.coefficients.drag.breakdown.compressible[wing.tag].total
        state.conditions.aerodynamics.coefficients.drag.breakdown.compressible[wing.tag].total = compressibility_drag * 1. # avoid linking variables
        total_compressibility_drag += compressibility_drag * (s_wing/S_ref)

    state.conditions.aerodynamics.coefficients.drag.breakdown.compressible.total  = total_compressibility_drag
        
    return total_compressibility_drag
