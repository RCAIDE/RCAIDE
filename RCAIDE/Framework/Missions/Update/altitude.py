# RCAIDE/Framework/Missions/Update/altitude.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field

# package imports
import numpy as np

# RCAIDE imports
import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
#  Update Altitude
# ----------------------------------------------------------------------------------------------------------------------


def update_altitude(State: rcf.State,
                    Settings: rcf.Settings,
                    System: rcf.System):

    State.freestream.altitude[:, 0] = State.frames.inertial.position[:, 2]
                   
    return State, Settings, System