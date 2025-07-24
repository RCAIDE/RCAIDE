# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/trim_drag.py
# 
# Created:  Mar 2025, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE
from RCAIDE.Framework.Core import Units
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Spolier Drag 
# ---------------------------------------------------------------------------------------------------------------------- 
def trim_drag(state,settings,geometry):
    """Updates the aerodynamic performance of an aircraft given the influence of deflected spoilers
  
    Parameters
    ----------
    state : Data
        flight conditions of aircraft
        
    settings : dict
        aerodynamic settings
        
    geometry : Data
        aircraft geometry 

    References
    ----------
    [1]  Croom, Delwin R. Low-speed wind-tunnel investigation of various segments of flight spoilers
         as trailing-vortex-alleviation devices on a transport aircraft model. No. NASA-TN-D-8162. 1976.
      
    """    
    # unpack   
    parasite_total        = state.conditions.aerodynamics.coefficients.drag.parasite.total            
    induced_total         = state.conditions.aerodynamics.coefficients.drag.induced.total            
    compressibility_total = state.conditions.aerodynamics.coefficients.drag.compressible.total     
    miscellaneous_drag    = state.conditions.aerodynamics.coefficients.drag.miscellaneous.total
    cooling_drag          = state.conditions.aerodynamics.coefficients.drag.cooling.total  
    form_drag             = state.conditions.aerodynamics.coefficients.drag.form.total   
    wave_drag             = state.conditions.aerodynamics.coefficients.drag.wave.total  

    # untrimmed drag 
    drag  =  parasite_total + induced_total  + compressibility_total + miscellaneous_drag + cooling_drag + form_drag + wave_drag
    
    trim_drag_coef =  np.zeros_like(drag)
    for wing in geometry.wings: 
        for cs in wing.control_surfaces:
            if type(cs) == RCAIDE.Library.Components.Wings.Control_Surfaces.Spoiler:
                trim_drag_coef += drag * (0.0011 * (cs.deflection / Units.degrees))  
                state.conditions.aerodynamics.coefficients.lift.total  +=  -0.0075 *(cs.deflection / Units.degrees)  
                state.conditions.static_stability.coefficients.M       +=  0.0053 *(cs.deflection / Units.degrees)  
    
    state.conditions.aerodynamics.coefficients.drag.trim.total =  trim_drag_coef 
    return  
