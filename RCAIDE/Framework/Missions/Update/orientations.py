# RCAIDE/Framework/Missions/Update/orientations.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field
from typing import Tuple

# package imports
import numpy as np
from scipy.spatial.transform import Rotation as T

# RCAIDE imports
import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
#  Update Orientations
# ----------------------------------------------------------------------------------------------------------------------

def angles_to_dcms(rotations: np.ndarray, sequence: Tuple[int] = (2, 1, 0)) -> np.ndarray:

    def

def update_orientations(State: rcf.State,
                        Settings: rcf.Settings,
                        System: rcf.System):

    v_inertial = State.frames.inertial.velocity
    body_intertial_rotations = State.frames.body.inertial_rotations

    ###---Body Frame Rotations---###

    phi = body_intertial_rotations[:, 0, None]

    # Body Frame Transformation Matrices
    T_inertial_to_body =
                   
    return State, Settings, System