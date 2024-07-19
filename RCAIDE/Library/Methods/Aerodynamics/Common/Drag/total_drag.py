# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/total_drag.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  Wave Drag 
# ---------------------------------------------------------------------------------------------------------------------- 
def total_drag(state,settings,geometry):
    """ Computes the total drag of an aircraft.

    Assumptions:
        None

    Source:
        None 

    Args:
        settings.
          drag_coefficient_increment                          (float): drag_coefficient_increment [Unitless]
          lift_to_drag_adjustment                             (float): lift_to_drag_adjustment    [Unitless]  
        state.conditions.aerodynamics.coefficients.drag.
          trim_corrected_drag                         (numpy.ndarray): trim corrected drag        [Unitless]
          spoiler_drag                                (numpy.ndarray): spoiler drag               [Unitless]
        geometry                                               (dict): aircraft data structure    [-]


    Returns:
        None 
    """    

    # Unpack inputs 
    drag =  state.conditions.aerodynamics.coefficients.drag

    drag_coefficient_increment = settings.drag_coefficient_increment
    trim_corrected_drag        = drag.trim_corrected_drag
    spoiler_drag               = drag.spoiler_drag 

    # Add drag_coefficient_increment
    aircraft_total_drag = trim_corrected_drag + drag_coefficient_increment + spoiler_drag
    drag.drag_coefficient_increment = drag_coefficient_increment
    
    # Add L/D correction
    aircraft_total_drag  = aircraft_total_drag/(1.+settings.lift_to_drag_adjustment) 

    # Store to results 
    drag.total           = aircraft_total_drag
    
    return  