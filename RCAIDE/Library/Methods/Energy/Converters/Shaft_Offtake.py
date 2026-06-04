# RCAIDE/Library/Methods/Propulsors/Converters/shaft_offtake.py
# (c) Copyright 2025 Aerospace Research Community LLC
#
# Created: Mar, 2025, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT 
# ----------------------------------------------------------------------------------------------------------------------
from __future__ import annotations
# package imports
import jax.numpy as np

# RCAIDE imports

from typing import TYPE_CHECKING
if TYPE_CHECKING:
        import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
# shaft_offtake
# ----------------------------------------------------------------------------------------------------------------------


def func_shaft_offtake(
        power,
        T_ref,
        P_ref,
        T_t_ref,
        P_t_ref,
        mdhc
):

        core_massflow = mdhc * np.sqrt(T_ref / T_t_ref) * (P_t_ref / P_ref)
        work = np.divide(power, core_massflow,
                         out=np.zeros_like(power), where=core_massflow != 0)  # Handle div-by-zero with ufunc

        return work


def shaft_offtake(
        state: "rcf.State",
        system: "rcf.System",
        settings: "rcf.Settings",
) -> ("rcf.State", "rcf.Aircraft", "rcf.Settings"):

        # Get Inputs
        shaft = system.energy.propulsors.shaft_offtake
        power = shaft.power_draw
        T_ref = shaft.reference_temperature
        P_ref = shaft.reference_pressure

        T_t_ref = system.energy.reference_temperature
        P_t_ref = system.energy.reference_pressure

        mdhc    = system.energy.compressor_nondimensional_massflow

        # Call Function

        work = func_shaft_offtake(power, T_ref, P_ref, T_t_ref, P_t_ref, mdhc)

        # Set Input State
        # N/A - Shaft offtake is derived from system parameters, not performance state

        # Set Output State

        outputs = state.energy.converters.shaft_offtake.outputs
        outputs.work = work

        return state, system, settings