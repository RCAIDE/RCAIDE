# RCAIDE/Library/Methods/Propulsors/moment.py
# (c) Copyright 2025 Aerospace Research Community LLC
#
# Created: Apr 2025, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# package imports

import jax.numpy as np

# RCAIDE imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
#  Turbofan Moment
# ----------------------------------------------------------------------------------------------------------------------


def func_propulsor_moment(
        propulsor_thrust: np.ndarray,
        propulsor_origin: np.ndarray,
        vehicle_center_of_gravity: np.ndarray
):

    moment_arm = propulsor_origin - vehicle_center_of_gravity
    moment = np.cross(moment_arm, propulsor_thrust)

    return moment


def propulsor_moment(state: "rcf.State",
                     system: "rcf.System",
                     settings: "rcf.Settings",
                     ):

    vehicle_center_of_gravity = system.mass_properties.center_of_gravity

    for idx, propulsor in enumerate(system.energy.propulsors):

        propulsor_thrust = state.energy.propulsors[idx].thrust
        propulsor_origin = system.energy.propulsors[idx].origin

        moment = func_propulsor_moment(propulsor_thrust, propulsor_origin, vehicle_center_of_gravity)

        state.energy.propulsors[idx].moment = moment

    return state, system, settings
