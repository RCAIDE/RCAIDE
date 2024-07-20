# RCAIDE/Library/Missions/Common/Update/aerodynamics.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Update Aerodynamics
# ----------------------------------------------------------------------------------------------------------------------
def aerodynamics(segment):
    """ Computes the aerodynamic properties of the aircraft 
            segment.state.conditions.aerodynamics.coefficients.lift        [unitless]
            segment.state.conditions.aerodynamics.coefficients.drag        [unitless]
            segment.state.conditions.frames.wind.force_vector              [newtons]
            segment.state.conditions.frames.wind.drag_force_vector         [newtons]
    
        Assumptions:
            +X out nose
            +Y out starboard wing
            +Z down

        Args: 
            segment.analyses.aerodynamics                                     [Function]
            segment.analyses.aerodynamics.settings.maximum_lift_coefficient   [unitless]
            segment.analyses.aerodynamics.geometry.reference_area             [meter^2]
            segment.state.conditions.freestream.dynamic_pressure              [pascals]

        Returns:
            None
    """
    
    # unpack
    conditions         = segment.state.conditions
    aerodynamics_model = segment.analyses.aerodynamics
    q                  = segment.state.conditions.freestream.dynamic_pressure
    Sref               = aerodynamics_model.geometry.reference_area
    CLmax              = aerodynamics_model.settings.maximum_lift_coefficient
    
    # call aerodynamics model
    results = aerodynamics_model.evaluate(segment)    
    
    # unpack results
    CL = results.lift.total
    CD = results.drag.total

    CL[q<=0.0] = 0.0
    CD[q<=0.0] = 0.0
    
    # CL limit
    CL[CL>CLmax] = CLmax 
    CL[CL< -CLmax] = -CLmax
        
    # dimensionalize
    F = segment.state.ones_row(3) * 0.0

    F[:,2] = ( -CL * q * Sref )[:,0]
    F[:,0] = ( -CD * q * Sref )[:,0]
 
    # pack conditions
    conditions.aerodynamics.coefficients.lift.total  = CL
    conditions.aerodynamics.coefficients.drag.total  = CD
    conditions.frames.wind.force_vector[:,:]         = F[:,:]

    return