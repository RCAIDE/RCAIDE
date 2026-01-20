# RCAIDE/Library/Methods/Stability/Vortex_Lattice_Method/evaluate_VLM.py
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports      
from RCAIDE.Library.Methods.Mass_Properties.Center_of_Gravity.update_center_of_gravity import update_center_of_gravity
from RCAIDE.Library.Methods.Mass_Properties.Moment_of_Inertia.update_moments_of_inertia import update_moments_of_inertia

import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Vortex_Lattice
# ---------------------------------------------------------------------------------------------------------------------- 
def evaluate(state,settings,vehicle):
    """Evaluates static margin and neutral point using built surrogates 
    
    Assumptions: 
        
    Source:
        None

    Args:
        stability    : VLM analysis  [unitless]
        state        : flight conditions     [unitless]
        settings     : VLM analysis settings [unitless]
        vehicle      : vehicle configuration [unitless] 
        
    Returns: 
        None  
    """ 
    # update center of gravity
    if settings.update_center_of_gravity: 
        update_center_of_gravity(state, vehicle)
     
    # update static margin 
    c_ref                                                   = vehicle.reference_chord   
    state.conditions.static_stability.static_margin   = np.atleast_2d((vehicle.neutral_point  - state.conditions.weights.vehicle.global_center_of_gravity[:,0]) / c_ref).T         
        
    # update moment of inertia
    if settings.update_moments_of_inertia: 
        update_moments_of_inertia(state, vehicle)
    
    return  