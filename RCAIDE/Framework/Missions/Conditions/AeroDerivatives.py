# RCAIDE/Framework/Missions/Conditions/AeroDerivatives.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import field

# package imports
import numpy as np

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  AeroDerivatives
# ----------------------------------------------------------------------------------------------------------------------


@dataclasses(kw_only=True)
class AeroDerivativesConditions(Conditions):

    #Attribute      Type        Default Value
    name:           str         = 'Aerodynamic Derivatives'

    dCL_dAlpha:     np.ndarrary = field(default_factory=lambda: np.ndarrary((1, 1)))
    dCL_dBeta:      np.ndarrary = field(default_factory=lambda: np.ndarrary((1, 1)))
    dCL_dV:         np.ndarrary = field(default_factory=lambda: np.ndarrary((1, 1)))
    dCL_dThrottle:  np.ndarrary = field(default_factory=lambda: np.ndarrary((1, 1)))

    dCD_dAlpha:     np.ndarrary = field(default_factory=lambda: np.ndarrary((1, 1)))
    dCD_dBeta:      np.ndarrary = field(default_factory=lambda: np.ndarrary((1, 1)))
    dCD_dV:         np.ndarrary = field(default_factory=lambda: np.ndarrary((1, 1)))
    dCD_dThrottle:  np.ndarrary = field(default_factory=lambda: np.ndarrary((1, 1)))