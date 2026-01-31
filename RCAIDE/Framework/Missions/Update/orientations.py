# RCAIDE/Framework/Missions/Update/orientations.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from copy import deepcopy

# package imports
import RNUMPY as rp
from RNUMPY.scipy.spatial.transform import Rotation as T

# RCAIDE imports
import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
#  Update Orientations
# ----------------------------------------------------------------------------------------------------------------------


def update_orientations(state: "rcf.State",
                        system: "rcf.System",
                        settings: "rcf.Settings",
                        ):

    v_inertial = state.frames.inertial.velocity_vector

    # ---Body Frame Rotations---

    body_inertial_rotations = state.frames.body.inertial_rotations

    phi = body_inertial_rotations[:, 0, None]

    # Body Frame Transformation Matrices

    try:
        TI2B = T.from_euler('zyx', body_inertial_rotations)
        TB2I = TI2B.inv()
    except Exception as e:
        print(f"Error in calculating body frame rotations: {e}")


    # Velocity Transformation
    v_body = TI2B.apply(v_inertial)

    # X-Z Projection of velocity
    v_xz = deepcopy(v_body)
    v_xz[:, 1] = 0
    v_xz_mag = rp.sqrt(rp.sum(v_xz))

    # Angle of Attack
    alpha = rp.arctan2(v_xz[:, 2], v_xz[:, 0])

    # Side Slip Angle
    beta = rp.arctan2(v_body[:, 1], v_xz_mag)

    # ---Wind Frame Rotations---

    wind_body_rotations = rp.zeros_like(body_inertial_rotations)
    wind_body_rotations[:, 0] = 0.        # No x-axis roll in wind frame
    wind_body_rotations[:, 1] = alpha     # Theta is Angle of Attack
    wind_body_rotations[:, 2] = beta      # Psi is Side Slip Angle

    TW2B = T.from_euler('zyx', wind_body_rotations)
    TW2I = TW2B * TB2I

    # ---Pack Results---

    state.aerodynamics.angles.alpha[:, 0] = alpha
    state.aerodynamics.angles.beta[:, 0] = beta
    state.aerodynamics.angles.phi = phi

    state.frames.body.transform_to_inertial = TB2I
    state.frames.wind.transform_to_inertial = TW2I

    state.frames.wind.body_rotations = wind_body_rotations
                   
    return state, system, settings
