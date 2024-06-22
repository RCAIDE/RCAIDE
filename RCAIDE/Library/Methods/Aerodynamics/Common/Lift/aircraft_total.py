## @ingroup Library-Methods-Aerodynamics-Common-Lift
# RCAIDE/Library/Methods/Aerodynamics/Common/Lift/aircraft_total.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Mar 2024 M. Carke     


# ----------------------------------------------------------------------
#  Aircraft Total
# ----------------------------------------------------------------------
## @ingroup Library-Methods-Aerodynamics-Common-Fidelity_Zero-Lift 
def aircraft_total(state,settings,geometry):
    """Returns the total aircraft lift of the aircraft 

    Assumptions:
    None

    Source:
    None

    Args:
    state.conditions.aerodynamics.coefficients.lift    [Unitless]

    Returns:
    aircraft_lift_total (lift coefficient)            [Unitless]


    """      
    
    aircraft_lift_total = state.conditions.aerodynamics.coefficients.lift

    return aircraft_lift_total
