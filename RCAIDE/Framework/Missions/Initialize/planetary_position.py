# RCAIDE/Framework/Missions/Initialization/planetary_position.py
# (c) Copyright 2024 Aerospace Research Community LLC
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE Imports
import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
# Initialize Planetary Position
# ----------------------------------------------------------------------------------------------------------------------


def initialize_planetary_position(state: "rcf.State",
                                  system: "rcf.System",
                                  settings: "rcf.Settings",
                                  ):

    state.frames.planet.longitude = state.frames.planet.longitude.at[:,0].set(state.initials.frames.planet.longitude[-1, 0])
    state.frames.planet.latitude = state.frames.planet.latitude.at[:, 0].set(state.initials.frames.planet.latitude[-1, 0])

    return state, system, settings
