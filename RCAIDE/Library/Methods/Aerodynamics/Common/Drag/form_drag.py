# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/form_drag.py 
# 
# Created:  Jul 2025, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
  
from RCAIDE.Framework.Core   import Units 
from scipy.interpolate       import RegularGridInterpolator

# package imports
import numpy as np

# ---------------------------------------------------------------------------------------------------------------------- 
#  Form Drag 
# ----------------------------------------------------------------------------------------------------------------------   
def form_drag(state,settings,geometry):
    """Computes the form drag associated with an aircraft  
    """ 

    conditions    = state.conditions   
    Mach          = conditions.freestream.mach_number 
    alpha         = conditions.aerodynamics.angles.alpha   
    CD_form_total = np.zeros_like(Mach)
    
    for wing in geometry.wings: 
        #CD_form             = (3.2636* (alpha**2) - 0.0295* (alpha) - 0.0007)*( 1.1765 * Mach)
        CD_form             =( 54.865* (alpha**4) - 5.9437* (alpha**3) + 2.4156* (alpha**2) + 0.031* (alpha)  + 0.0001 )*( 1.1765 * Mach)
        CD_form[Mach>1]     = 0
        CD_form[CD_form<0]  = 0
        CD_form_total       += CD_form * (wing.areas.reference / geometry.reference_area) 
    state.conditions.aerodynamics.coefficients.drag.form.total = CD_form_total 
    return