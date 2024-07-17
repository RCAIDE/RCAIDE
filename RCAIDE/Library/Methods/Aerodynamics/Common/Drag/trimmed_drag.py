# trim.py
#
# Created:  Jan 2014, T. Orra
# Modified: Jan 2016, E. Botero  

# ----------------------------------------------------------------------
#  Computes the trim drag
# ----------------------------------------------------------------------
def trimmed_drag(state,settings,geometry):
    """Adjusts aircraft drag based on a trim correction

    Assumptions:
        None

    Source:
        None 

    Args:
        settings.trim_drag_correction_factor               (float):  trim_drag_correction_factor   [Unitless]
        state.conditions.aerodynamics.coefficients.
                          drag.breakdown.untrimmed (numpy.ndarray): untrimmed drag [Unitless]
        geometry                                            (dict): aircraft data structure [-]
    
    Returns:
        None 
    """    

    # unpack inputs  
    trim_correction_factor  = settings.trim_drag_correction_factor    
    untrimmed_drag          = state.conditions.aerodynamics.coefficients.drag.breakdown.untrimmed
    
    # trim correction
    corrected_aircraft_total_trim_drag = trim_correction_factor * untrimmed_drag
    
    state.conditions.aerodynamics.coefficients.drag.breakdown.trim_corrected_drag                  = corrected_aircraft_total_trim_drag    
    state.conditions.aerodynamics.coefficients.drag.breakdown.miscellaneous.trim_correction_factor = trim_correction_factor

    return  