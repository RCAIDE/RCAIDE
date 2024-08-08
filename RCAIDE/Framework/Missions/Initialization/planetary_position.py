# RCAIDE/Framework/Missions/Initialization/planetary_position.py
# (c) Copyright 2024 Aerospace Research Community LLC
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------

# package imports
import numpy as np

# RCAIDE Imports
import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
# Initialize Planetary Position
# ----------------------------------------------------------------------------------------------------------------------


def initialize_planetary_position(State: rcf.State,
                                  Settings: rcf.Settings,
                                  System: rcf.System):

    State.frames.planet.longitude[:, 0] = State.initials.frames.planet.longitude[-1, 0]
    State.frames.planet.latitude[:, 0]  = State.initials.frames.planet.latitude[-1, 0]

    return State, Settings, System
