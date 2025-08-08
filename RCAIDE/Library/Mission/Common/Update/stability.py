# RCAIDE/Library/Missions/Common/Update/stability.py
# 
# 
# Created:  Jul 2023, M. Clarke 
 
import RCAIDE
from RCAIDE.Library.Methods.Stability.compute_dynamic_flight_modes import compute_dynamic_flight_modes
# ----------------------------------------------------------------------------------------------------------------------
#  Stability
# ---------------------------------------------------------------------------------------------------------------------- 
def stability(segment): 
    """ Updates the stability of the aircraft 
        
        Assumptions:
        If stability model is defined, overwrite the aerodynamics calculations
        
        Inputs:
            None 
                 
        Outputs: 
            None
      
        Properties Used:
        N/A
                    
    """   
    # unpack
    stability_model    = segment.analyses.stability 

    vertical_fligth_flag = False
    if isinstance(segment,RCAIDE.Framework.Mission.Segments.Vertical_Flight.Climb) or \
       isinstance(segment,RCAIDE.Framework.Mission.Segments.Vertical_Flight.Hover) or \
       isinstance(segment,RCAIDE.Framework.Mission.Segments.Vertical_Flight.Descent):
        vertical_fligth_flag = True
        
    if stability_model != None and vertical_fligth_flag != True: 
        compute_dynamic_flight_modes(segment.state,stability_model.settings,stability_model.vehicle) 

    return