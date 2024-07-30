# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/induced_drag_aircraft.py 
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE
from RCAIDE.Framework.Core import Data

# package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Induced Drag Aircraft
# ---------------------------------------------------------------------------------------------------------------------- 
def induced_drag(state,settings,geometry):
    """Determines induced drag for the full aircraft

    Assumptions:
    This function operates in one of three ways:
       -An oswald efficiency is provided. All induced drag, inviscid and viscous, is use calculated using that factor
       -A span efficiency is provided. The inviscid induced drag is calculated from that. Viscous induced drag is
            calculated using the viscous_lift_dependent_drag_factor, K, and the parasite drag.
       -The inviscid induced drag from the the lift calculation for each wing, usually a vortex lattice, is used. Viscous induced drag is
            calculated using the viscous_lift_dependent_drag_factor, K, and the parasite drag.
            
        The last two options do not explicitly provide for the case where the fuselage produces an induced drag directly.

    Source:
    adg.stanford.edu (Stanford AA241 A/B Course Notes)
    http://aerodesign.stanford.edu/aircraftdesigNoneircraftdesign.html

    Args: 
        state.aero.lift.breakdown 
            .inviscid_wings[wings.*.tag]                            (numpy.ndarray): inviscid lift coefficient              [unitless]
        state.aero.drag.breakdown  
            .induced.inviscid                                       (numpy.ndarray): total inviscid induced drag coefficient [unitless]
            .induced.inviscid_wings[wings.*.tag]                    (numpy.ndarray): inviscid induced drag coefficient       [unitless]
            .parasite[wings.*.tag].parasite_drag        (numpy.ndarray): parasitic drag coefficient              [unitless]
            .parasite[wings.*.tag].reference_area                           (float): reference area                          [m^2]
        settings.
            .oswald_efficiency_factor                                       (float): oswald_efficiency_factor                [unitless]
            .viscous_lift_dependent_drag_factor                             (float): viscous_lift_dependent_drag_factor      [unitless]
            .span_efficiency                                                (float): span_efficiency                         [unitless] 

    Returns:
        state.aero.drag.breakdown   
            .induced.total                                          (numpy.ndarray): total induced drag coefficient          [unitless]
            .induced.viscous                                        (numpy.ndarray): viscous coefficient                     [unitless]
            .induced.oswald_efficiency_factor                       (numpy.ndarray): oswald_efficiency_factor coefficient    [unitless]
            .induced.viscous_wings_drag                             (numpy.ndarray): viscous_wings_drag coefficient          [unitless]  
    """
    # unpack inputs  
    wings         = geometry.wings 
    K             = settings.viscous_lift_dependent_drag_factor
    e_osw         = settings.oswald_efficiency_factor	 
    aero          = state.conditions.aerodynamics.coefficients
    CL            = aero.lift.total
    CDi           = aero.drag.induced.inviscid

    wing_viscous_induced_drags = Data()

    # If the oswald efficiency factor is not specified  
    if e_osw == None:

        # Prime totals
        area                        = 1E-12 
        AR                          = 1E-12 
        total_induced_viscous_drag  = K*aero.drag.parasite.total*(CL**2)

        # Go through each wing, and make calculations
        for wing in wings: 
            AR_wing    = wing.aspect_ratio
            S_wing     = aero.drag.parasite[wing.tag].reference_area  
            if S_wing > area:
                area = S_wing
                AR   = AR_wing

        # compute total induced drag 
        total_induced_drag = total_induced_viscous_drag +  CDi  

        # Calculate the vehicle level oswald efficiency
        e_osw = (CL**2)/(np.pi*AR*total_induced_drag)

    # If the user specifies a vehicle level oswald efficiency factor
    else: 
        # Find the largest wing, use that for AR
        S  = 1E-12 
        AR = 1E-12 
        for wing in wings:
            if wing.areas.reference>S:
                AR = wing.aspect_ratio
                S  = wing.areas.reference 

        # Calculate the induced drag       
        total_induced_drag = CL **2 / (np.pi*AR*e_osw)
        total_induced_viscous_drag = total_induced_drag - CDi

    aero.drag.induced.total                    = total_induced_drag
    aero.drag.induced.viscous                  = total_induced_viscous_drag
    aero.drag.induced.oswald_efficiency_factor = e_osw
    aero.drag.induced.viscous_wings_drag       = wing_viscous_induced_drags 
    return  
 