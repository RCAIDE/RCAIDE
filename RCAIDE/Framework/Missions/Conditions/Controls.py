# RCAIDE/Framework/Missions/Conditions/Controls.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field

# package imports
import numpy as np

# RCAIDE imports
from RCAIDE.Framework.Conditions import Conditions
from RCAIDE.Reference.Components import Component

# ----------------------------------------------------------------------------------------------------------------------
#  Controls
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class DynamicsVariables(Conditions):

    name:       str         = 'Dynamics'

    force_x:    bool        = False
    force_y:    bool        = False
    force_z:    bool        = False

    moment_x:   bool        = False
    moment_y:   bool        = False
    moment_z:   bool        = False


@dataclass(kw_only=True)
class ControlVariable(Conditions):

    #Attribute      Type        Default Value
    name:           str         = 'Control Variable'
    active:         bool        = False
    initial_guess:  float       = None

    value:          np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))


@dataclass(kw_only=True)
class SurfaceControlVariable(Conditions):

    #Attribute  Type            Default Value
    name:       str             = 'Surface Control Variable'
    surfaces:   list[Component] = field(default_factory=list)


@dataclass(kw_only=True)
class PropulsionControlVariable(Conditions):

    #Attribute  Type            Default Value
    name:       str             = 'Propulsion Control Variable'
    propulsors: list[Component] = field(default_factory=list)


@dataclass(kw_only=True)
class ControlsConditions(Conditions):

    name:           str                         = 'Controls'

    dynamics:       DynamicsVariables           = DynamicsVariables()

    body_angle:     ControlVariable             = ControlVariable(name='Body Angle')
    bank_angle:     ControlVariable             = ControlVariable(name='Bank Angle')
    wind_angle:     ControlVariable             = ControlVariable(name='Wind Angle')

    elapsed_time:   ControlVariable             = ControlVariable(name='Elapsed Time')
    velocity:       ControlVariable             = ControlVariable(name='Velocity')
    acceleration:   ControlVariable             = ControlVariable(name='Velocity')
    altitude:       ControlVariable             = ControlVariable(name='Altitude')

    thrust:         PropulsionControlVariable   = PropulsionControlVariable(name='Thrust Vector')
    throttle:       PropulsionControlVariable   = PropulsionControlVariable(name='Throttle')

    elevator:       SurfaceControlVariable      = SurfaceControlVariable(name='Elevator Deflection')
    rudder:         SurfaceControlVariable      = SurfaceControlVariable(name='Rudder Deflection')
    flaps:          SurfaceControlVariable      = SurfaceControlVariable(name='Flap Deflection')
    slats:          SurfaceControlVariable      = SurfaceControlVariable(name='Slat Deflection')
    ailerons:       SurfaceControlVariable      = SurfaceControlVariable(name='Aileron Deflection')





