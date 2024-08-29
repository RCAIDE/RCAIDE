# RCAIDE/Framework/Missions/Update/orientations.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field
from typing import Tuple
from copy import deepcopy

# package imports
import numpy as np
from scipy.spatial.transform import Rotation as T

# RCAIDE imports
import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
#  Update Orientations
# ----------------------------------------------------------------------------------------------------------------------


def update_orientations(State: rcf.State,
                        Settings: rcf.Settings,
                        System: rcf.System):

    v_inertial = State.frames.inertial.velocity

    # ---Body Frame Rotations---

    body_inertial_rotations = State.frames.body.inertial_rotations

    phi = body_inertial_rotations[:, 0, None]

    # Body Frame Transformation Matrices
    TI2B = T.from_euler('zyx', body_inertial_rotations)
    TB2I = TI2B.inv()

    # Velocity Transformation
    v_body = TI2B.apply(v_inertial)

    # X-Z Projection of velocity
    v_xz = deepcopy(v_body)
    v_xz[:, 1] = 0
    v_xz_mag = np.sqrt(np.sum(v_xz))[:, None]

    # Angle of Attack
    alpha = np.arctan2(v_xz[:, 2], v_xz[:, 0])[:, None]

    # Side Slip Angle
    beta = np.arctan2(v_body[:, 1], v_xz_mag[:, 0])[:, None]

    # ---Wind Frame Rotations---

    wind_body_rotations = np.zeros_like(body_inertial_rotations)
    wind_body_rotations[:, 0] = 0.              # No x-axis roll in wind frame
    wind_body_rotations[:, 1] = alpha[:, 0]     # Theta is Angle of Attack
    wind_body_rotations[:, 2] = beta[:, 0]      # Psi is Side Slip Angle

    TW2B = T.from_euler('zyx', wind_body_rotations)
    TW2I = TW2B * TB2I

    # ---Pack Results---

    State.aerodynamics.angle_of_attack[:, 0] = alpha[:, 0]
    State.aerodynamics.side_slip_angle[:, 0] = beta[:, 0]
    State.aerodynamics.roll_angle[:, 0] = phi[:, 0]

    State.frames.body.transform_to_inertial = TB2I
    State.frames.wind.transform_to_inertial = TW2I

    State.frames.wind.body_rotations = wind_body_rotations
                   
    return State, Settings, System
