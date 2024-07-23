# RCAIDE/Library/Missions/Segments/Common/Update/dimensionless.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Update Differentials Altitude
# ----------------------------------------------------------------------------------------------------------------------  
def differentials_altitude(segment):
    """ Initializes the differntial altitude and computes the discretized time steps.
    
        Assumptions: 
            None
        
        Args: 
            segment  : flight segment        [-] 
            
        Returns:
            None
    """

    # unpack
    t = segment.state.numerics.dimensionless.control_points 
    I = segment.state.numerics.dimensionless.integrate
    r = segment.state.conditions.frames.inertial.position_vector
    v = segment.state.conditions.frames.inertial.velocity_vector

    dz = r[-1,2] - r[0,2]
    
    # get overall time step
    dt = np.dot( I[-1,:] * dz , 1/v[:,2])

    # rescale operators
    t = t * dt

    # pack
    t_initial = segment.state.conditions.frames.inertial.time[0,0]
    segment.state.conditions.frames.inertial.time[:,0] = t_initial + t[:,0]

    return