## @ingroup Library-Missions-Segments-Common-Update
# RCAIDE/Library/Missions/Segments/Common/Update/differentials_time.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  Update Differentials Time
# ----------------------------------------------------------------------------------------------------------------------

## @ingroup Library-Missions-Segments-Common-Update
def differentials_time(segment):
    """ Updates the time descretization 
        
        Assumptions:
            None
        
        Args:
            segment.state.conditions:
                .frames.inertial.time         [s]
        Returns:
            segment.state.numerics.time
                .control_points               [s]
                .differentiate                [-]
                .integrate                    [-]
 
    """    
    
    # unpack
    numerics = segment.state.numerics
    x        = numerics.dimensionless.control_points
    D        = numerics.dimensionless.differentiate
    I        = numerics.dimensionless.integrate
    
    # rescale time
    time = segment.state.conditions.frames.inertial.time
    T    = time[-1] - time[0]
    t    = x * T
    
    # rescale operators
    D = D / T
    I = I * T
    
    # pack
    numerics.time.control_points = t
    numerics.time.differentiate  = D
    numerics.time.integrate      = I

    return
