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
    initials:           Self                        = None
    numerics:           Numerics                    = field(default_factory=lambda: Numerics())

    frames:             FrameConditions             = field(default_factory=lambda: FrameConditions())
    freestream:         FreestreamConditions        = field(default_factory=lambda: FreestreamConditions())

    mass:               MassConditions              = field(default_factory=lambda: MassConditions())
    energy:             NetworkConditions           = field(default_factory=lambda: NetworkConditions())

    aerodynamics:       AerodynamicsConditions      = field(default_factory=lambda: AerodynamicsConditions())
    controls:           ControlsConditions          = field(default_factory=lambda: ControlsConditions())

    unknowns:           Conditions                  = field(default_factory=lambda: Conditions(name='Unknowns'))
    residuals:          Conditions                  = field(default_factory=lambda: Conditions(name='Residuals'))

    def __post_init__(self):
        self.initials = State(name='Initial State')
