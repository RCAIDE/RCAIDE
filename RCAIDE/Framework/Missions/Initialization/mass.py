# RCAIDE/Framework/Missions/Initialization/mass.py
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
# Initialize Mass
# ----------------------------------------------------------------------------------------------------------------------


def initialize_mass(State: rcf.State,
                    Settings: rcf.Settings,
                    System: rcf.System):

    m_initial = State.initials.mass.total[-1, 0]
    m_current = State.mass.total[0, 0]

    State.mass.total += (m_initial - m_current)

    return State, Settings, System
