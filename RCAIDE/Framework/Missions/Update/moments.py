# RCAIDE/Framework/Missions/Update/moments.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug, 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT 
# ----------------------------------------------------------------------------------------------------------------------

import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
# Update Moments
# ----------------------------------------------------------------------------------------------------------------------


def update_moments(
        State: rcf.State,
        Settings: rcf.Settings,
        System: rcf.System
        ):

        wind = State.frames.wind.total_moment
        thrust = State.energy.total_moment

        TW2I = State.frames.wind.transform_to_inertial

        M = TW2I.apply(wind)

        State.frames.inertial.total_moment = M + thrust
        
        return State, Settings, System