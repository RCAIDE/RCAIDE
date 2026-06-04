# RCAIDE/Framework/Missions/Conditions/Controls.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from typing import Literal

# package imports
import equinox as eqx
import jax.numpy as jnp

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import Conditions
from RCAIDE.Framework.Missions.Conditions.Stability import StabilityConditions

from RCAIDE.Library import Component

# ----------------------------------------------------------------------------------------------------------------------
#  Controls
# ----------------------------------------------------------------------------------------------------------------------


def get_active(Conditions):
    """
    Returns the active controls/residuals
    """

    return [c for c in vars(Conditions).values() if hasattr(c, 'active') and c.active]


def count_active(Conditions):
    """
    counts the number of active controls/residuals in the given Conditions object
    """

    return len(get_active(Conditions))


class DynamicResidual(Conditions):

    tag:    str         = eqx.field(static=True, default='Dynamic Residual')
    type:   str | None  = eqx.field(static=True, default=None)
    active: bool        = eqx.field(static=True, default=False)
    index:  int | None  = eqx.field(static=True, default=None)

    value:  jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty(0))

ResidualNames = Literal[
    "force_x", "force_y", "force_z",
    "moment_x", "moment_y", "moment_z",
]

class DynamicsConditions(Conditions):
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

    tag:        str             = eqx.field(static=True, default='Dynamics')

    force_x:    DynamicResidual = eqx.field(default_factory=lambda: DynamicResidual(tag='force_x', type='force', index=0))
    force_y:    DynamicResidual = eqx.field(default_factory=lambda: DynamicResidual(tag='force_y', type='force', index=1))
    force_z:    DynamicResidual = eqx.field(default_factory=lambda: DynamicResidual(tag='force_z', type='force', index=2))
    moment_x:   DynamicResidual = eqx.field(default_factory=lambda: DynamicResidual(tag='moment_x', type='moment', index=0))
    moment_y:   DynamicResidual = eqx.field(default_factory=lambda: DynamicResidual(tag='moment_y', type='moment', index=1))
    moment_z:   DynamicResidual = eqx.field(default_factory=lambda: DynamicResidual(tag='moment_z', type='moment', index=2))

    def get_active_residuals(self) -> list:
        return get_active(self)

    def count_active_residuals(self) -> int:
        return count_active(self)


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

    # Attribute     Type                        Default Value
    tag:            str                         = eqx.field(static=True, default='Control Variable')

    active:         bool                        = False
    initial_guess:  float | jnp.ndarray | None  = None

    value:          jnp.ndarray                 = eqx.field(default_factory=lambda: jnp.empty(0))

    def get_field_name(self):
        return self.tag.replace(' ', '_').lower()


class DirectControlVariable(ControlVariable):

    # Attribute     Type            Default Value
    tag:            str             = eqx.field(static=True, default='Direct Control Variable')

    path:           tuple[str, ...] = eqx.field(static=True, default_factory=tuple)
    path_indices:   tuple | None    = eqx.field(static=True, default_factory=lambda: (slice(None), 0))


class SurfaceControlVariable(ControlVariable):
    """
    Represents a control variable for a surface in an aircraft or vehicle.

    This class defines the properties of a surface control variable, including its name,
    associated surfaces, deflection, and static stability characteristics. It inherits from
    the Conditions class and uses keyword-only arguments.

    Attributes
    ----------
    tag : str
        The name of the aerodunamic control variable. Defaults to 'Surface Control Variable'.
    surfaces : list[Component]
        A list of surfaces associated with the control variable. Defaults to None.
    deflection : np.ndarray
        An array representing the deflection of the surface. Initialized as a 1x1 zero array.
    static_stability : StaticCoefficients
        An object representing the static stability characteristics of the surface.

    Returns
    -------
    SurfaceControlVariable
        An instance of the SurfaceControlVariable class with the specified attributes.
    """

    #Attribute          Type                        Default Value
    tag:                str                         = eqx.field(static=True, default='Surface Control Variable')
    surfaces:           tuple[Component] | None     = None

    stability:          StabilityConditions         = eqx.field(default_factory=StabilityConditions)


class EnergyControlVariable(ControlVariable):
    """
    Represents a control variable for propulsion systems in a vehicle or aircraft.

    This class defines the properties of a propulsion control variable, including its name
    and associated propulsors. It inherits from the Conditions class and uses keyword-only arguments.

    Attributes
    ----------
    name : str
        The name of the propulsion control variable. Defaults to 'Propulsion Control Variable'.
    """

    #Attribute  Type            Default Value
    tag:        str             = eqx.field(static=True, default='Energy Control Variable')

    value:      jnp.ndarray     = eqx.field(default_factory=lambda: jnp.empty(0))


def _default_bank_angle():
    return DirectControlVariable(
        tag='Bank Angle', 
        path=('frames', 'body', 'inertial_rotations'), 
        path_indices=(slice(None), 0)
    )

def _default_body_angle():
    return DirectControlVariable(
        tag='Body Angle', 
        path=('frames', 'body', 'inertial_rotations'), 
        path_indices=(slice(None), 1)
    )

def _default_velocity():
    return DirectControlVariable(
        tag='Velocity', 
        path=('frames', 'inertial', 'velocity_vector'), 
        path_indices=(slice(None), 0)
    )

def _default_altitude():
    return DirectControlVariable(
        tag='Altitude', 
        path=('frames', 'inertial', 'position_vector'), 
        path_indices=(slice(None), 2)
    )

class ControlsConditions(Conditions):

    tag:           str                      = eqx.field(static=True, default='Controls')

    bank_angle:     DirectControlVariable   = eqx.field(default_factory=_default_bank_angle)
    body_angle:     DirectControlVariable   = eqx.field(default_factory=_default_body_angle)
    wind_angle:     DirectControlVariable   = eqx.field(default_factory=lambda: DirectControlVariable(tag='Wind Angle'))

    elapsed_time:   DirectControlVariable   = eqx.field(default_factory=lambda: DirectControlVariable(tag='Elapsed Time'))
    velocity:       DirectControlVariable   = eqx.field(default_factory=_default_velocity)
    acceleration:   DirectControlVariable   = eqx.field(default_factory=lambda: DirectControlVariable(tag='Velocity'))
    altitude:       DirectControlVariable   = eqx.field(default_factory=_default_altitude)

    custom_controls:        tuple = eqx.field(default_factory=tuple)
    active_routing_table:   tuple = eqx.field(static=True, default=())


    def add_control_variable(self, control_variable: ControlVariable) -> None:
        new_custom_controls = self.custom_controls + (control_variable,)
        return eqx.tree_at(lambda c: c.custom_controls, self, new_custom_controls)

    def __getattr__(self, item: str):
        if item.startswith("__") and item.endswith("__"):
            raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{item}'")

        for ctrl in self.custom_controls:
            # Assuming ControlVariable has a get_field_name() method
            if ctrl.get_field_name() == item:
                return ctrl

        raise AttributeError(f"'{self.tag}' has no explicit or custom control named '{item}'")

    def get_active_controls(self) -> tuple:
        active_list = []

        # 1. Check explicit controls
        for field in self.__dataclass_fields__:
            control_var = getattr(self, field)
            # Ensure it's actually a control variable and is active
            if getattr(control_var, 'active', False):
                active_list.append(control_var)

        # 2. Check custom controls
        for control_var in self.custom_controls:
            if getattr(control_var, 'active', False):
                active_list.append(control_var)

        # Return as an immutable tuple for JAX safety
        return tuple(active_list)

    def count_active_controls(self) -> int:
        return len(self.get_active_controls())