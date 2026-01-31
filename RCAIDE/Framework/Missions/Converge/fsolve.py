# RCAIDE/Framework/Missions/Converge/fsolve.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug, 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT 
# ----------------------------------------------------------------------------------------------------------------------

from typing import Tuple

# package imports
import RNUMPY as rp


# RCAIDE imports
import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
# fsolve Convergence
# ----------------------------------------------------------------------------------------------------------------------


def fsolve_results_parser(
        fsolve_result: Tuple,
        state: "rcf.State",
        system: "rcf.System",
        settings: "rcf.Settings",
) -> ("rcf.State", "rcf.System", "rcf.Settings"):

        unknowns:       rp.ndarray      = fsolve_result[0]
        infodict:       dict            = fsolve_result[1]
        ier:            int             = fsolve_result[2]
        mesg:           str             = fsolve_result[3]

        if ier != 1:
            print("Segment Convergence Failed:", mesg)
            state.numerics.converged = False
        else:
            print("Segment Converged.")
            print("Number of function evaluations:", infodict['nfev'])
            state.unknowns = unknowns
            state.unpack_unknowns()
            state.numerics.converged = True
        
        return state, system, settings

def fsolve_update_kwargs(
        fsolve_kwargs: dict,
        state: "rcf.State",
        system: "rcf.System",
        settings: "rcf.Settings",
):

        fsolve_kwargs['x0'] = state.unknowns
        fsolve_kwargs['args'] = (state, system, settings)

        return fsolve_kwargs