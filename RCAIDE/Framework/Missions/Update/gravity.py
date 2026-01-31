# RCAIDE/Framework/Missions/gravity.py
# (c) Copyright 2026 Aerospace Research Community LLC#
# Created:  Jan 2026, E. Botero
# Modified: 
# -------------------------------------------------------------------------------
#  Imports
# -------------------------------------------------------------------------------

# RCAIDE Imports

import RCAIDE.Framework as rcf

import RNUMPY as rp


# -------------------------------------------------------------------------------
#  Stateful/Framework Version
# -------------------------------------------------------------------------------


def update_gravity(
    state: "rcf.State",
    system: "rcf.System",
    settings: "rcf.Settings",
):
    """
    Updates the current gravity as applied to the system
    """

    # UPDATE ME
    state.freestream.gravity = state.freestream.gravity.at[:,0].set(-9.81)


    return state, system, settings