## @ingroup Library-Missions-Segments-Common-Update
# RCAIDE/Library/Missions/Common/Update/forces.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
from RCAIDE.Framework.Core  import  orientation_product
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Update Forces
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Missions-Segments-Common-Update
def forces(segment): 
    """ Updates the total resultant force on the vehicle 
        
        Assumptions:
            None
        
        Args:
            segment.state.conditions.:
                frames.wind.force_vector               [N]
                frames.body.thrust_force_vector        [N]
                frames.inertial.gravity_force_vector   [N]
        Returns:
            segment.conditions
                frames.inertial.total_force_vector     [N] 
    """    

    # unpack
    RT                            = segment.reverse_thrust_ratio
    conditions                    = segment.state.conditions 
    wind_force_vector             = conditions.frames.wind.force_vector
    body_thrust_force_vector      = conditions.frames.body.thrust_force_vector
    inertial_gravity_force_vector = conditions.frames.inertial.gravity_force_vector

    # unpack transformation matrices
    T_body2inertial = conditions.frames.body.transform_to_inertial
    T_wind2inertial = conditions.frames.wind.transform_to_inertial

    # to inertial frame
    F = orientation_product(T_wind2inertial,wind_force_vector)
    T = orientation_product(T_body2inertial,body_thrust_force_vector)
    W = inertial_gravity_force_vector

    # sum of the forces
    F_tot = F +  T*(1 - RT) + W + T*RT

    # pack
    conditions.frames.inertial.total_force_vector[:,:] = F_tot[:,:]

    return
 