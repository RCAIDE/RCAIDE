# RCAIDE/Framework/Missions/Converge/fsolve.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug, 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT 
# ----------------------------------------------------------------------------------------------------------------------

from typing import Tuple

# package imports
import numpy as np


# RCAIDE imports
import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
# fsolve Convergence
# ----------------------------------------------------------------------------------------------------------------------


def fsolve_results_parser(
        fsolve_result: Tuple,
        State: rcf.State,
        Settings: rcf.Settings,
        System: rcf.System
        ):

        unknowns:       np.ndarray      = fsolve_result[0]
        infodict:       dict            = fsolve_result[1]
        ier:            int             = fsolve_result[2]
        mesg:           str             = fsolve_result[3]

        if ier != 1:
            print("Segment Convergence Failed:", mesg)
            State.numerics.converged = False
        else:
            print("Segment Converged.")
            print("Number of function evaluations:", infodict['nfev'])
            State.numerics.converged = True
        
        return State, Settings, System