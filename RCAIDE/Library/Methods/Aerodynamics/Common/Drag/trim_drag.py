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
    [2]   Sadraey, Mohammad H. Aircraft performance: an engineering approach. CRC Press, 2017.
      
    """    
    # unpack   
    parasite_total          = state.conditions.aerodynamics.coefficients.drag.parasite.total            
    induced_total           = state.conditions.aerodynamics.coefficients.drag.induced.total            
    compressibility_total   = state.conditions.aerodynamics.coefficients.drag.compressible.total    
    form_drag               = state.conditions.aerodynamics.coefficients.drag.form.total  

    # untrimmed drag 
    CD_0  =  parasite_total + induced_total  + compressibility_total + form_drag
    
    # control surface drag 
    control_surface_drag = np.zeros_like(CD_0)
    for wing in geometry.wings: 
        for cs in wing.control_surfaces:
            if type(cs) == RCAIDE.Library.Components.Wings.Control_Surfaces.Spoiler:
                control_surface_drag += CD_0 * (0.0011 * (cs.deflection / Units.degrees))  
                state.conditions.aerodynamics.coefficients.lift.total  +=  -0.0075 *(cs.deflection / Units.degrees)  
                state.conditions.static_stability.coefficients.M       +=  0.0053 *(cs.deflection / Units.degrees)
                
            if type(cs) == RCAIDE.Library.Components.Wings.Control_Surfaces.Flap:
                if cs.type ==  'split':
                    A = 0.0014
                    B = 1.5
                elif cs.type ==  'plain':
                    A = 0.0016
                    B = 1.5
                elif cs.type ==  'single_slotted':
                    A = 0.00018
                    B = 2
                elif cs.type ==  'flowler':
                    A = 0.00015
                    B = 1.5 
                elif cs.type ==  'double_slotted':
                    A = 0.0011
                    B = 1     
                else:
                    A = 0.0011
                    B = 1                     
                control_surface_drag += cs.chord_fraction * A * (state.conditions.control_surfaces.flap.deflection **B )
                     
            if type(cs) == RCAIDE.Library.Components.Wings.Control_Surfaces.Slat:
                control_surface_drag += cs.chord_fraction * CD_0  
     
    state.conditions.aerodynamics.coefficients.drag.trim.total =  control_surface_drag 
    return  
