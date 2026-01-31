# RCAIDE/Framework/Missions/Conditions/Controls.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import unittest
import chex
from dataclasses import field

# package imports
import RNUMPY as rp
import numpy as np

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


@chex.dataclass(kw_only=True)
class DynamicResidual(Conditions):

    tag:    str     = 'Dynamic Residual'
    type:   str     = None
    active: bool    = False
    index:  int     = None

    value:          rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))


@chex.dataclass(kw_only=True)
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

    tag:        str             = 'Dynamics'

    force_x:    DynamicResidual = field(default_factory=lambda: DynamicResidual(tag='F_x', type='force', index=0))
    force_y:    DynamicResidual = field(default_factory=lambda: DynamicResidual(tag='F_y', type='force', index=1))
    force_z:    DynamicResidual = field(default_factory=lambda: DynamicResidual(tag='F_z', type='force', index=2))
    moment_x:   DynamicResidual = field(default_factory=lambda: DynamicResidual(tag='M_x', type='moment', index=0))
    moment_y:   DynamicResidual = field(default_factory=lambda: DynamicResidual(tag='M_y', type='moment', index=1))
    moment_z:   DynamicResidual = field(default_factory=lambda: DynamicResidual(tag='M_z', type='moment', index=2))

    def get_active_residuals(self) -> list:
        return get_active(self)

    def count_active_residuals(self) -> int:
        return count_active(self)


@chex.dataclass(kw_only=True)
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
    value : rp.ndarray
        The current value of the control variable. Initialized as a 1x1 zero array.

    """

    # Attribute     Type                Default Value
    tag:            str                 = 'Control Variable'

    active:         bool                = False
    initial_guess:  float | rp.ndarray  = None

    value:          rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    def get_field_name(self):
        return self.tag.replace(' ', '_').lower()


@chex.dataclass(kw_only=True)
class DirectControlVariable(ControlVariable):

    # Attribute     Type                Default Value
    tag:            str                 = 'Direct Control Variable'

    path:           tuple[str, ...]     = None
    path_indices:   tuple               = None


@chex.dataclass(kw_only=True)
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
    deflection : rp.ndarray
        An array representing the deflection of the surface. Initialized as a 1x1 zero array.
    static_stability : StaticCoefficients
        An object representing the static stability characteristics of the surface.

    Returns
    -------
    SurfaceControlVariable
        An instance of the SurfaceControlVariable class with the specified attributes.
    """

    #Attribute          Type                Default Value
    tag:                str                 = 'Surface Control Variable'
    surfaces:           list[Component]     = None

    stability:          StabilityConditions = field(default_factory=lambda: StabilityConditions())


@chex.dataclass(kw_only=True)
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
    tag:       str             = 'Energy Control Variable'

    value:      rp.ndarray      = field(default_factory=lambda: rp.zeros((1, 1)))


@chex.dataclass(kw_only=True)
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
    residuals : DynamicsConditions
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

    tag:           str                      = 'Controls'

    bank_angle:     DirectControlVariable   = field(default_factory=lambda: DirectControlVariable(tag='Bank Angle'))
    body_angle:     DirectControlVariable   = field(default_factory=lambda: DirectControlVariable(tag='Body Angle'))
    wind_angle:     DirectControlVariable   = field(default_factory=lambda: DirectControlVariable(tag='Wind Angle'))

    elapsed_time:   DirectControlVariable   = field(default_factory=lambda: DirectControlVariable(tag='Elapsed Time'))
    velocity:       DirectControlVariable   = field(default_factory=lambda: DirectControlVariable(tag='Velocity'))
    acceleration:   DirectControlVariable   = field(default_factory=lambda: DirectControlVariable(tag='Velocity'))
    altitude:       DirectControlVariable   = field(default_factory=lambda: DirectControlVariable(tag='Altitude'))

    def __post_init__(self):

        # Map body angle to the Y-axis of the body frame
        self.body_angle.path = ('frames', 'body', 'inertial_rotations')
        self.body_angle.path_indices = (slice(None), 1)

        # Map bank angle to the X-axis of the body frame
        self.bank_angle.path = ('frames', 'body', 'inertial_rotations')
        self.bank_angle.path_indices = (slice(None), 0)

        # Map velocity to the X-axis of the inertial frame
        self.velocity.path = ('frames', 'inertial', 'velocity_vector')
        self.velocity.path_indices = (slice(None), 0)

        # Map altitude to the Z-axis of the inertial frame
        self.altitude.path = ('frames', 'inertial', 'position_vector')
        self.altitude.path_indices = (slice(None), 2)

    def add_control_variable(self, control_variable: ControlVariable) -> None:
        if isinstance(control_variable, ControlVariable):
            setattr(self, control_variable.get_field_name(), control_variable)
        else:
            raise TypeError(f'Attempted to add a control variable to {self.tag} '
                            f"which was not a ControlVariable data structure.")

    def get_active_controls(self) -> list:
        return get_active(self)

    def count_active_controls(self) -> int:
        return count_active(self)


class TestDynamicsVariables(unittest.TestCase):
    def test_default_values(self):
        dv = DynamicsConditions()
        self.assertEqual(dv.tag, 'Dynamics')
        self.assertFalse(dv.force_x)
        self.assertFalse(dv.force_y)
        self.assertFalse(dv.force_z)
        self.assertFalse(dv.moment_x)
        self.assertFalse(dv.moment_y)
        self.assertFalse(dv.moment_z)

    def test_custom_values(self):
        dv = DynamicsConditions(force_x=True, moment_z=True)
        self.assertTrue(dv.force_x)
        self.assertFalse(dv.force_y)
        self.assertTrue(dv.moment_z)


class TestControlVariable(unittest.TestCase):
    def test_default_values(self):
        cv = ControlVariable()
        self.assertEqual(cv.tag, 'Control Variable')
        self.assertFalse(cv.active)
        self.assertIsNone(cv.initial_guess)
        np.testing.assert_array_equal(cv.value, rp.zeros((1, 1)))

    def test_custom_values(self):
        cv = ControlVariable(tag='Test', active=True, initial_guess=5.0)
        self.assertEqual(cv.tag, 'Test')
        self.assertTrue(cv.active)
        self.assertEqual(cv.initial_guess, 5.0)


class TestSurfaceControlVariable(unittest.TestCase):
    def test_default_values(self):
        scv = SurfaceControlVariable()
        self.assertEqual(scv.tag, 'Surface Control Variable')
        np.testing.assert_array_equal(scv.deflection, rp.zeros((1, 1)))
        self.assertIsInstance(scv.static_stability, StaticCoefficients)


class TestPropulsionControlVariable(unittest.TestCase):
    def test_default_values(self):
        pcv = EnergyControlVariable()
        self.assertEqual(pcv.tag, 'Propulsion Control Variable')
        np.testing.assert_array_equal(pcv.value, rp.zeros((1, 1)))


class TestControlsConditions(unittest.TestCase):
    def test_default_values(self):
        cc = ControlsConditions()
        self.assertEqual(cc.tag, 'Controls')
        self.assertIsInstance(cc.residuals, DynamicsConditions)
        self.assertIsInstance(cc.body_angle, ControlVariable)
        self.assertIsInstance(cc.thrust, EnergyControlVariable)
        self.assertIsInstance(cc.elevator, SurfaceControlVariable)

    def test_custom_values(self):
        cc = ControlsConditions(tag='Custom Controls')
        self.assertEqual(cc.tag, 'Custom Controls')
        self.assertEqual(cc.body_angle.tag, 'Body Angle')
        self.assertEqual(cc.thrust.tag, 'Thrust')
        self.assertEqual(cc.elevator.tag, 'Elevator Controls')


if __name__ == '__main__':
    unittest.main()
