# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/form_drag.py 
# 
# Created:  Jul 2025, M. Clarke 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
import RCAIDE
from  RCAIDE.Framework.Core import  Units
from RCAIDE.Library.Methods.Utilities         import Cubic_Spline_Blender

# ---------------------------------------------------------------------------------------------------------------------- 
#  Form Drag 
# ----------------------------------------------------------------------------------------------------------------------   
def form_drag(state,settings,geometry):
    """Computes the form drag associated with an aircraft  
    """ 

    conditions       = state.conditions   
    Mach             = conditions.freestream.mach_number
    low_mach_cutoff  = settings.supersonic.begin_drag_rise_mach_number 
    high_mach_cutoff = settings.supersonic.end_drag_rise_mach_number 

    sub_spline = Cubic_Spline_Blender(low_mach_cutoff, high_mach_cutoff)  
    sub_h00    = lambda M:sub_spline.compute(M)
    
    alpha     = conditions.aerodynamics.angles.alpha 
    CD_form   = 0
    for wing in geometry.wings:
        M_correction = 2.9788*(Mach **3) - 6.4381*(Mach **2) + 4.4967*(Mach)  
        if type(wing) !=  RCAIDE.Library.Components.Wings.Vertical_Tail():
            CD_form_wing =  0 
            if len(wing.segments) > 0:
                CD_sep    = 0
                for i in  range((len(wing.segments) -1)):
                    segs          = list(wing.segments.keys())
                    segment       = wing.segments[segs[i]]
                    CD_sep        = (111.41* (alpha**4) - 16.569* (alpha**3) + 1.8* (alpha**2) - 0.0242*alpha + 0.0015)*M_correction
                    CD_form_wing  += CD_sep   * segment.areas.reference  
            else:
                CD_sep  = (111.41* (alpha**4) - 16.569* (alpha**3) + 1.8* (alpha**2) - 0.0242*alpha + 0.0015)*M_correction
                CD_form_wing = CD_sep * wing.areas.reference  
        
            CD_form += CD_form_wing /geometry.reference_area 
        
    state.conditions.aerodynamics.coefficients.drag.form.total = CD_form * sub_h00(Mach)
    return