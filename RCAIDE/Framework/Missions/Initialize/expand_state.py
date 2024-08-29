# RCAIDE/Framework/Missions/Initialization/expand_state.py
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
#  Expand State
# ----------------------------------------------------------------------------------------------------------------------


def expand_state(State: rcf.State,
                 Settings: rcf.Settings,
                 System: rcf.System):

    State.expand_rows(rows=State.numerics.number_of_control_points)

    return State, Settings, System
