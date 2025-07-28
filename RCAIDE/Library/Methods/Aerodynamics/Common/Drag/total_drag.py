# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/total_drag.py
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
        state.conditions.aerodynamics.coefficients.drag. 
        geometry                                               (dict): aircraft data structure    [-]


    Returns:
        None 
    """

    # unpack inputs    
    drag                 = state.conditions.aerodynamics.coefficients.drag

    # various drag components
    parasite_total        = drag.parasite.total            
    induced_total         = drag.induced.total            
    compressibility_total = drag.compressible.total     
    miscellaneous_drag    = drag.miscellaneous.total
    cooling_drag          = drag.cooling.total 
    trim_drag             = drag.trim.total  
    form_drag             = drag.form.total  
    wave_drag             = drag.wave.total  
 
    # total drag 
    drag.total =  settings.trim_drag_correction_factor * (parasite_total + induced_total  + compressibility_total + miscellaneous_drag \
                  + cooling_drag + trim_drag + form_drag + wave_drag     + settings.drag_coefficient_increment)  

    return  