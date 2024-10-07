# RCAIDE/Framework/State.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field
from typing import Self

# package imports
import numpy as np

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import *

# ----------------------------------------------------------------------------------------------------------------------
#  State
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class State(Conditions):

    # Attribute         Type                        Default Value
    name:               str                         = 'State'
    numerics:           Numerics                    = Numerics()
    initials:           Self                        = None

    frames:             FrameConditions             = FrameConditions()
    freestream:         FreestreamConditions        = FreestreamConditions()

    mass:               MassConditions              = MassConditions()
    energy:             NetworkConditions           = NetworkConditions()

    aerodynamics:       AerodynamicsConditions      = AerodynamicsConditions()
    aero_derivatives:   AeroDerivativesConditions   = AeroDerivativesConditions()

    controls:           ControlsConditions          = ControlsConditions()

    unknowns:           Conditions                  = Conditions(name='Unknowns')
    residuals:          Conditions                  = Conditions(name='Residuals')

    def __post_init__(self):
        self.initials = State(name='Initial State')
