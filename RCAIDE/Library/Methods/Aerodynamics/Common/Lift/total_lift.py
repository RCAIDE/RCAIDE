## @ingroup Library-Methods-Aerodynamics-Common-Lift
# RCAIDE/Library/Methods/Aerodynamics/Common/Lift/total_lift.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Mar 2024 M. Carke     

# ----------------------------------------------------------------------------------------------------------------------
#  Total Lift 
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Aerodynamics-Common-Fidelity_Zero-Lift 
def total_lift(state,settings,geometry):
    """Returns the total lift of the aircraft 

    Assumptions:
        None

    Source:
        None

    Args: 
        state    (dict): flight conditions [-]
        settings (dict): analyses settings [-]
        geometry (dict): aircraft geometry [-]
        
    Returns:
        state.conditions.aerodynamics.coefficients.lift (numpy.ndarray): lift coefficient [unitless]  
    """      
     
    return state.conditions.aerodynamics.coefficients.lift.total
