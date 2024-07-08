# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/untrimmed_drag.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  Untrmmed drag 
# ----------------------------------------------------------------------------------------------------------------------
def untrimmed_drag(state,settings,geometry):
    """Sums aircraft drag before trim correction

    Assumptions:
        None

    Source:
        None

    Args:
        state.conditions.aerodynamics.coefficients.drag.breakdown.
          parasite.total            (numpy.ndarray) : total parasite drag      [Unitless]
          induced.total             (numpy.ndarray) : total induced drag       [Unitless]
          compressible.total        (numpy.ndarray) : total compressible drag  [Unitless]
          miscellaneous.total       (numpy.ndarray) : total miscellaneous drag [Unitless]

    Returns:
        None 
    """       

    # unpack inputs
    conditions     = state.conditions

    # various drag components
    parasite_total        = conditions.aerodynamics.coefficients.drag.breakdown.parasite.total            
    induced_total         = conditions.aerodynamics.coefficients.drag.breakdown.induced.total            
    compressibility_total = conditions.aerodynamics.coefficients.drag.breakdown.compressible.total         
    miscellaneous_drag    = conditions.aerodynamics.coefficients.drag.breakdown.miscellaneous.total 

    # untrimmed drag 
    conditions.aerodynamics.coefficients.drag.breakdown.untrimmed =  parasite_total + induced_total  + compressibility_total + miscellaneous_drag
    return  
