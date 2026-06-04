# RCAIDE/Framework/Missions/Initialization/mass.py
# (c) Copyright 2024 Aerospace Research Community LLC
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE Imports
import equinox as eqx
import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
# Initialize Mass
# ----------------------------------------------------------------------------------------------------------------------


def initialize_mass(state: "rcf.State",
                    system: "rcf.System",
                    settings: "rcf.Settings",
                    ):

    m_initial = state.initials.mass.total[-1, 0]

    # This needs to be set automatically if the initial value is 0
    if m_initial==0.0:
        m_initial = system.mass_properties.total

    m_current = state.mass.total[0, 0]

    state = eqx.tree_at(
        lambda s:s.mass.total,
        state,
        state.mass.total + (m_initial - m_current)
    )

    return state, system, settings
