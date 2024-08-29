# RCAIDE/Framework/Missions/Update/forces.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug, 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT 
# ----------------------------------------------------------------------------------------------------------------------

import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
# Update Forces
# ----------------------------------------------------------------------------------------------------------------------


def update_forces(
        State: rcf.State,
        Settings: rcf.Settings,
        System: rcf.System
        ):
        
        wind    = State.frames.wind.total_force
        thrust  = State.frames.body.thrust_force
        gravity = State.frames.inertial.gravity_force

        TB2I = State.frames.body.transform_to_inertial
        TW2I = State.frames.wind.transform_to_inertial

        F = TW2I.apply(wind)
        T = TB2I.apply(thrust)

        State.frames.inertial.total_force = F + T + gravity
        
        return State, Settings, System