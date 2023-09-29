## @ingroup Methods-Missions-Common-Update 
# RCAIDE/Methods/Missions/Common/Update/aerodynamics.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Update Aerodynamics
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Missions-Common-Update
def aerodynamics(segment):
    """ Gets aerodynamics conditions
    
        Assumptions:
        +X out nose
        +Y out starboard wing
        +Z down

        Inputs:
            segment.analyses.aerodynamics_model                    [Function]
            aerodynamics_model.settings.maximum_lift_coefficient   [unitless]
            aerodynamics_model.geometry.reference_area             [meter^2]
            segment.state.conditions.freestream.dynamic_pressure   [pascals]

        Outputs:
            conditions.aerodynamics.coefficients.lift [unitless]
            conditions.aerodynamics.coefficients.drag [unitless]
            conditions.frames.wind.lift_force_vector [newtons]
            conditions.frames.wind.drag_force_vector [newtons]

        Properties Used:
        N/A
    """
    
    # unpack
    conditions         = segment.state.conditions
    aerodynamics_model = segment.analyses.aerodynamics
    q                  = segment.state.conditions.freestream.dynamic_pressure
    Sref               = aerodynamics_model.geometry.reference_area
    CLmax              = aerodynamics_model.settings.maximum_lift_coefficient
    
    # call aerodynamics model
    results = aerodynamics_model( segment.state )    
    
    # unpack results
    CL = results.lift.total
    CD = results.drag.total

    CL[q<=0.0] = 0.0
    CD[q<=0.0] = 0.0
    
    # CL limit
    CL[CL>CLmax] = CLmax
    
    CL[CL< -CLmax] = -CLmax
        
    # dimensionalize
    L = segment.state.ones_row(3) * 0.0
    D = segment.state.ones_row(3) * 0.0

    L[:,2] = ( -CL * q * Sref )[:,0]
    D[:,0] = ( -CD * q * Sref )[:,0]

    results.lift_force_vector = L
    results.drag_force_vector = D    

    # pack conditions
    conditions.aerodynamics.coefficients.lift     = CL
    conditions.aerodynamics.coefficients.drag     = CD
    conditions.frames.wind.lift_force_vector[:,:] = L[:,:] # z-axis
    conditions.frames.wind.drag_force_vector[:,:] = D[:,:] # x-axis
