# RCAIDE/Framework/State.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field

# package imports
import numpy as np

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import *

# ----------------------------------------------------------------------------------------------------------------------
#  State
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class State(Conditions):

    #Attribute  Type        Default Value
    name:       str         = 'State'

    numerics:           Numerics                    = Numerics()

    frames:             FrameConditions             = FrameConditions()

    mass:               MassConditions              = MassConditions()
    energy:             EnergyConditions            = EnergyConditions()
    noise:              NoiseConditions             = NoiseConditions()

    aerodynamics:       AerodynamicsConditions      = AerodynamicsConditions()
    aero_derivatives:   AeroDerivativesConditions   = AeroDerivativesConditions()

    controls:           ControlsConditions          = ControlsConditions()
