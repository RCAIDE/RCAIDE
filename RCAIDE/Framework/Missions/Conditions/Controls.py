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
from RCAIDE.Framework.Missions.Conditions import Conditions, StaticCoefficients
from RCAIDE.Framework import Component

# ----------------------------------------------------------------------------------------------------------------------
#  Controls
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class DynamicsVariables(Conditions):
    """
    Represents the dynamics variables for a simulation.

    This class defines the forces and moments acting on an object in three-dimensional space.
    It inherits from the Conditions class and uses keyword-only arguments.

    Attributes
    ----------
    name : str
        The name of the dynamics object.
    force_x : bool
        Indicates if there's a force acting along the x-axis.
    force_y : bool
        Indicates if there's a force acting along the y-axis.
    force_z : bool
        Indicates if there's a force acting along the z-axis.
    moment_x : bool
        Indicates if there's a moment acting around the x-axis.
    moment_y : bool
        Indicates if there's a moment acting around the y-axis.
    moment_z : bool
        Indicates if there's a moment acting around the z-axis.
    """

    name:       str         = 'Dynamics'

    force_x:    bool        = False
    force_y:    bool        = False
    force_z:    bool        = False

    moment_x:   bool        = False
    moment_y:   bool        = False
    moment_z:   bool        = False


@dataclass(kw_only=True)
class ControlVariable(Conditions):
    """
    Represents a control variable in a simulation or control system.

    This class defines the properties of a control variable, including its name,
    activation status, initial guess, and current value. It inherits from the
    Conditions class and uses keyword-only arguments.

    Attributes
    ----------
    name : str
        The name of the control variable. Defaults to 'Control Variable'.
    active : bool
        Indicates whether the control variable is active or not. Defaults to False.
    initial_guess : float
        An initial guess for the control variable's value. Defaults to None.
    value : np.ndarray
        The current value of the control variable. Initialized as a 1x1 zero array.

    """

    #Attribute      Type        Default Value
    name:           str         = 'Control Variable'
    active:         bool        = False
    initial_guess:  float       = None

    value:          np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))


@dataclass(kw_only=True)
class SurfaceControlVariable(Conditions):
    """
    Represents a control variable for a surface in an aircraft or vehicle.

    This class defines the properties of a surface control variable, including its name,
    associated surfaces, deflection, and static stability characteristics. It inherits from
    the Conditions class and uses keyword-only arguments.

    Attributes
    ----------
    name : str
        The name of the surface control variable. Defaults to 'Surface Control Variable'.
    surfaces : list[Component]
        A list of Component objects representing the surfaces associated with this control variable.
    deflection : np.ndarray
        An array representing the deflection of the surface. Initialized as a 1x1 zero array.
    static_stability : StaticCoefficients
        An object representing the static stability characteristics of the surface.

    Returns
    -------
    SurfaceControlVariable
        An instance of the SurfaceControlVariable class with the specified attributes.
    """

    #Attribute          Type                Default Value
    name:               str                 = 'Surface Control Variable'

    surfaces:           list[Component]     = field(default_factory=list)

    deflection:         np.ndarray          = field(default_factory=lambda: np.zeros((1, 1)))

    static_stability:   StaticCoefficients  = field(default_factory=lambda: StaticCoefficients())


@dataclass(kw_only=True)
class PropulsionControlVariable(Conditions):
    """
    Represents a control variable for propulsion systems in a vehicle or aircraft.

    This class defines the properties of a propulsion control variable, including its name
    and associated propulsors. It inherits from the Conditions class and uses keyword-only arguments.

    Attributes
    ----------
    name : str
        The name of the propulsion control variable. Defaults to 'Propulsion Control Variable'.
    propulsors : list[Component]
        A list of Component objects representing the propulsors associated with this control variable.
    """

    #Attribute  Type            Default Value
    name:       str             = 'Propulsion Control Variable'

    propulsors: list[Component] = field(default_factory=list)


@dataclass(kw_only=True)
class ControlsConditions(Conditions):
    """
    Represents the control conditions for an aircraft or vehicle simulation.

    This class encapsulates various control variables and dynamics for a comprehensive
    simulation environment. It includes controls for aircraft orientation, propulsion,
    and surface controls.

    Attributes
    ----------
    name : str
        The name of the control conditions, default is 'Controls'.
    dynamics : DynamicsVariables
        Object representing the dynamic variables of the simulation.

    body_angle : ControlVariable
        Control variable for the body angle.
    bank_angle : ControlVariable
        Control variable for the bank angle.
    wind_angle : ControlVariable
        Control variable for the wind angle.

    elapsed_time : ControlVariable
        Control variable for the elapsed time.
    velocity : ControlVariable
        Control variable for velocity.
    acceleration : ControlVariable
        Control variable for acceleration (Note: named 'Velocity' in initialization).
    altitude : ControlVariable
        Control variable for altitude.

    thrust : PropulsionControlVariable
        Control variable for thrust vector.
    throttle : PropulsionControlVariable
        Control variable for throttle.

    elevator : SurfaceControlVariable
        Control variable for elevator surfaces.
    rudder : SurfaceControlVariable
        Control variable for rudder surfaces.
    flaps : SurfaceControlVariable
        Control variable for flap surfaces.
    slats : SurfaceControlVariable
        Control variable for slat surfaces.
    ailerons : SurfaceControlVariable
        Control variable for aileron surfaces.
    """

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

    elevator:       SurfaceControlVariable      = SurfaceControlVariable(name='Elevator Controls')
    rudder:         SurfaceControlVariable      = SurfaceControlVariable(name='Rudder Controls')
    flaps:          SurfaceControlVariable      = SurfaceControlVariable(name='Flap Controls')
    slats:          SurfaceControlVariable      = SurfaceControlVariable(name='Slat Controls')
    ailerons:       SurfaceControlVariable      = SurfaceControlVariable(name='Aileron Controls')





