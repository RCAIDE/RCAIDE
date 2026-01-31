# RCAIDE/Framework/Missions/Conditions/Stability.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  Import
# ----------------------------------------------------------------------------------------------------------------------

import unittest
import chex
from dataclasses import field

# package imports
import RNUMPY as rp
import numpy as np

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Stability
# ----------------------------------------------------------------------------------------------------------------------


@chex.dataclass(kw_only=True)
class StaticCoefficients(Conditions):
    """
    Static stability coefficients for an aircraft.

    This class encapsulates various aerodynamic coefficients and forces
    relevant to the static stability analysis of an aircraft.

    Attributes
    ----------
    name : str
        The name of the coefficient set.
    lift : rp.ndarray
        The lift coefficient. Shape: (1, 1)
    drag : rp.ndarray
        The drag coefficient. Shape: (1, 1)
    X : rp.ndarray
        The X-axis force coefficient. Shape: (1, 1)
    Y : rp.ndarray
        The Y-axis force coefficient. Shape: (1, 1)
    Z : rp.ndarray
        The Z-axis force coefficient. Shape: (1, 1)
    L : rp.ndarray
        The rolling moment coefficient. Shape: (1, 1)
    M : rp.ndarray
        The pitching moment coefficient. Shape: (1, 1)
    N : rp.ndarray
        The yawing moment coefficient. Shape: (1, 1)
    e : rp.ndarray
        The Oswald efficiency factor. Shape: (1, 1)

    Notes
    -----
    All coefficient arrays are initialized as 1x1 numpy arrays with zero values.
    These can be updated with actual coefficient values during analysis.
    """

    # Attribute     Type        Default Value
    tag:            str         = 'Static Stability Coefficients'

    lift:           rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    drag:           rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    X:              rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    Y:              rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    Z:              rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    L:              rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    M:              rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    N:              rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    e:              rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))


@chex.dataclass(kw_only=True)
class StaticForces(Conditions):
    """
    Static forces acting on an aircraft.

    This class encapsulates the static forces that are relevant to aircraft 
    stability analysis, including lift, drag, and forces in the X, Y, and Z directions.

    Attributes
    ----------
    name : str
        The name of the static forces set. Default is 'Static Stability Forces'.
    lift : rp.ndarray
        The lift force. Shape: (1, 1)
    drag : rp.ndarray
        The drag force. Shape: (1, 1)
    X : rp.ndarray
        The force in the X-direction. Shape: (1, 1)
    Y : rp.ndarray
        The force in the Y-direction. Shape: (1, 1)
    Z : rp.ndarray
        The force in the Z-direction. Shape: (1, 1)

    Notes
    -----
    All force arrays are initialized as 1x1 numpy arrays with zero values.
    These can be updated with actual force values during analysis.
    """

    # Attribute     Type        Default Value
    tag:           str         = 'Static Stability Forces'

    lift:           rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    drag:           rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    X:              rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    Y:              rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    Z:              rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))


@chex.dataclass(kw_only=True)
class StaticMoments(Conditions):
    """
    Represents the static moments acting on an aircraft.

    This class encapsulates the static moments that are relevant to aircraft 
    stability analysis, including rolling, pitching, and yawing moments.

    Attributes
    ----------
    name : str
        The name of the static moments set. Default is 'Static Stability Moments'.
    L : rp.ndarray
        The rolling moment. Shape: (1, 1)
    M : rp.ndarray
        The pitching moment. Shape: (1, 1)
    N : rp.ndarray
        The yawing moment. Shape: (1, 1)

    Notes
    -----
    All moment arrays are initialized as 1x1 numpy arrays with zero values.
    These can be updated with actual moment values during analysis.
    """

    # Attribute     Type        Default Value
    tag:           str         = 'Static Stability Moments'

    L:              rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    M:              rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    N:              rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))


@chex.dataclass(kw_only=True)
class CoefficientDerivatives(Conditions):
    """
    Represents the coefficient derivatives for static stability analysis of an aircraft.

    This class encapsulates various coefficient derivatives related to stability axis
    and body axis, which are crucial for analyzing the static stability characteristics
    of an aircraft.

    Attributes:
    ----------
    name : str
        The name of the coefficient derivatives set. Default is 'Coefficient Static Stability Derivatives'.
    
    alpha : rp.ndarray
        Derivative with respect to angle of attack. Shape: (1, 1)
    beta : rp.ndarray
        Derivative with respect to sideslip angle. Shape: (1, 1)
    
    delta_a : rp.ndarray
        Derivative with respect to aileron deflection. Shape: (1, 1)
    delta_e : rp.ndarray
        Derivative with respect to elevator deflection. Shape: (1, 1)
    delta_r : rp.ndarray
        Derivative with respect to rudder deflection. Shape: (1, 1)
    delta_f : rp.ndarray
        Derivative with respect to flap deflection. Shape: (1, 1)
    delta_s : rp.ndarray
        Derivative with respect to spoiler deflection. Shape: (1, 1)
    
    u : rp.ndarray
        Derivative with respect to forward velocity. Shape: (1, 1)
    v : rp.ndarray
        Derivative with respect to lateral velocity. Shape: (1, 1)
    w : rp.ndarray
        Derivative with respect to vertical velocity. Shape: (1, 1)
    
    p : rp.ndarray
        Derivative with respect to roll rate. Shape: (1, 1)
    q : rp.ndarray
        Derivative with respect to pitch rate. Shape: (1, 1)
    r : rp.ndarray
        Derivative with respect to yaw rate. Shape: (1, 1)

    Notes:
    -----
    All derivative arrays are initialized as 1x1 numpy arrays with zero values.
    These can be updated with actual derivative values during analysis.
    """

    # Attribute     Type        Default Value
    tag:            str         = 'Coefficient Static Stability Derivatives'

    # Throttle Derivative
    throttle:       rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    # Stability Axis Derivatives
    alpha:          rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    beta:           rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    delta_a:        rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    delta_e:        rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    delta_r:        rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    delta_f:        rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    delta_s:        rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    # Body Axis Derivatives

    u:              rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    v:              rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    w:              rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))

    p:              rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    q:              rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))
    r:              rp.ndarray  = field(default_factory=lambda: rp.zeros((1, 1)))


@chex.dataclass(kw_only=True)
class StaticDerivatives(Conditions):
    """
    Represents the static stability coefficient derivatives for an aircraft.

    This class encapsulates various coefficient derivatives related to static stability
    analysis, including lift, drag, and force/moment coefficients in different axes.

    Attributes:
    ----------
    name : str
        The name of the static derivatives set. Default is 'Static Stability Coefficients Derivatives'.
    Clift : CoefficientDerivatives
        Lift coefficient static stability derivatives.
    Cdrag : CoefficientDerivatives
        Drag coefficient static stability derivatives.
    CX : CoefficientDerivatives
        X-axis force coefficient static stability derivatives.
    CY : CoefficientDerivatives
        Y-axis force coefficient static stability derivatives.
    CZ : CoefficientDerivatives
        Z-axis force coefficient static stability derivatives.
    CL : CoefficientDerivatives
        Rolling moment coefficient static stability derivatives.
    CM : CoefficientDerivatives
        Pitching moment coefficient static stability derivatives.
    CN : CoefficientDerivatives
        Yawing moment coefficient static stability derivatives.

    Notes:
    -----
    All coefficient derivatives are instances of the CoefficientDerivatives class,
    allowing for detailed representation of stability characteristics in various axes and conditions.
    """

    # Attribute     Type        Default Value
    tag:            str         = 'Static Stability Coefficients Derivatives'

    Clift:  CoefficientDerivatives = field(default_factory=lambda:
                                           CoefficientDerivatives(tag='Lift Coefficient Static Stability Derivatives'))
    Cdrag:  CoefficientDerivatives = field(default_factory=lambda:
                                           CoefficientDerivatives(tag='Drag Coefficient Static Stability Derivatives'))

    CX:     CoefficientDerivatives = field(default_factory=lambda:
                                           CoefficientDerivatives(tag='X Coefficient Static Stability Derivatives'))
    CY:     CoefficientDerivatives = field(default_factory=lambda:
                                           CoefficientDerivatives(tag='Y Coefficient Static Stability Derivatives'))
    CZ:     CoefficientDerivatives = field(default_factory=lambda:
                                           CoefficientDerivatives(tag='Z Coefficient Static Stability Derivatives'))

    CL:     CoefficientDerivatives = field(default_factory=lambda:
                                           CoefficientDerivatives(tag='L Coefficient Static Stability Derivatives'))
    CM:     CoefficientDerivatives = field(default_factory=lambda:
                                           CoefficientDerivatives(tag='M Coefficient Static Stability Derivatives'))
    CN:     CoefficientDerivatives = field(default_factory=lambda:
                                           CoefficientDerivatives(tag='N Coefficient Static Stability Derivatives'))


@chex.dataclass(kw_only=True)
class StaticStability(Conditions):
    """
    Represents the static stability characteristics of an aircraft.

    This class encapsulates various components and parameters related to static stability analysis,
    including forces, moments, coefficients, derivatives, and stability metrics.

    Attributes:
    ----------
    name : str
        The name identifier for this static stability instance. Defaults to 'Static Stability'.
    forces : StaticForces
        An object representing the static forces acting on the aircraft.
    moments : StaticMoments
        An object representing the static moments acting on the aircraft.
    coefficients : StaticCoefficients
        An object containing the static stability coefficients.
    derivatives : StaticDerivatives
        An object containing the static stability derivatives.
    static_margin : rp.ndarray
        The static margin of the aircraft. Shape: (1, 1)
    neutral_point : rp.ndarray
        The neutral point of the aircraft. Shape: (1, 1)
    spiral_criteria : rp.ndarray
        The spiral stability criteria. Shape: (1, 1)
    pitch_rate : rp.ndarray
        The pitch rate of the aircraft. Shape: (1, 1)
    roll_rate : rp.ndarray
        The roll rate of the aircraft. Shape: (1, 1)
    yaw_rate : rp.ndarray
        The yaw rate of the aircraft. Shape: (1, 1)

    Notes:
    -----
    All numpy array attributes are initialized as 1x1 arrays with zero values.
    These can be updated with actual values during stability analysis.
    """

    tag:                str                 = 'Static Stability'
    
    forces:             StaticForces        = field(default_factory=lambda: StaticForces())
    moments:            StaticMoments       = field(default_factory=lambda: StaticMoments())
    
    coefficients:       StaticCoefficients  = field(default_factory=lambda: StaticCoefficients())
    derivatives:        StaticDerivatives   = field(default_factory=lambda: StaticDerivatives())
    
    static_margin:      rp.ndarray          = field(default_factory=lambda: rp.zeros((1, 1)))
    neutral_point:      rp.ndarray          = field(default_factory=lambda: rp.zeros((1, 1)))
    spiral_criteria:    rp.ndarray          = field(default_factory=lambda: rp.zeros((1, 1)))
    
    pitch_rate:         rp.ndarray          = field(default_factory=lambda: rp.zeros((1, 1)))
    roll_rate:          rp.ndarray          = field(default_factory=lambda: rp.zeros((1, 1)))
    yaw_rate:           rp.ndarray          = field(default_factory=lambda: rp.zeros((1, 1)))


@chex.dataclass(kw_only=True)
class DynamicStability(Conditions):
    """
    Represents the dynamic stability characteristics of an aircraft.

    This class encapsulates the longitudinal and lateral dynamic modes of an aircraft,
    which are crucial for analyzing its dynamic stability behavior.

    Attributes:
    ----------
    name : str
        The name identifier for this dynamic stability instance. Defaults to 'Dynamic Stability'.
    LongModes : Conditions
        An object representing the longitudinal modes of the aircraft's dynamic stability.
        Initialized with a name 'Longitudinal Modes'.
    LatModes : Conditions
        An object representing the lateral modes of the aircraft's dynamic stability.
        Initialized with a name 'Lateral Modes'.

    Notes:
    -----
    This class inherits from the Conditions base class and uses the dataclass decorator
    with kw_only=True, meaning all attributes must be specified as keyword arguments when instantiating.
    """

    #Attribute      Type        Default Value
    tag:            str         = 'Dynamic Stability'

    LongModes:      Conditions  = field(default_factory=lambda: Conditions(tag='Longitudinal Modes'))
    LatModes:       Conditions  = field(default_factory=lambda: Conditions(tag='Lateral Modes'))



@chex.dataclass(kw_only=True)
class StabilityConditions(Conditions):
    """
    Represents the overall stability conditions of an aircraft, including both static and dynamic stability.

    This class encapsulates both static and dynamic stability characteristics of an aircraft,
    providing a comprehensive view of its stability properties.

    Attributes:
    ----------
    name : str
        The name identifier for this stability conditions instance. Defaults to 'Stability'.
    static : StaticStability
        An instance of StaticStability representing the static stability characteristics of the aircraft.
    dynamic : DynamicStability
        An instance of DynamicStability representing the dynamic stability characteristics of the aircraft.

    Notes:
    -----
    This class inherits from the Conditions base class and uses the dataclass decorator
    with kw_only=True, meaning all attributes must be specified as keyword arguments when instantiating.
    """

    # Attribute     Type                Default Value
    tag:            str                 = 'Stability'

    static:         StaticStability     = field(default_factory=lambda: StaticStability())
    dynamic:        DynamicStability    = field(default_factory=lambda: DynamicStability())


class TestStaticCoefficients(unittest.TestCase):
    def test_default_values(self):
        sc = StaticCoefficients()
        self.assertEqual(sc.tag, 'Static Stability Coefficients')
        np.testing.assert_array_equal(sc.lift, rp.zeros((1, 1)))
        np.testing.assert_array_equal(sc.drag, rp.zeros((1, 1)))
        np.testing.assert_array_equal(sc.X, rp.zeros((1, 1)))
        np.testing.assert_array_equal(sc.Y, rp.zeros((1, 1)))
        np.testing.assert_array_equal(sc.Z, rp.zeros((1, 1)))
        np.testing.assert_array_equal(sc.L, rp.zeros((1, 1)))
        np.testing.assert_array_equal(sc.M, rp.zeros((1, 1)))
        np.testing.assert_array_equal(sc.N, rp.zeros((1, 1)))
        np.testing.assert_array_equal(sc.e, rp.zeros((1, 1)))


class TestStaticForces(unittest.TestCase):
    def test_default_values(self):
        sf = StaticForces()
        self.assertEqual(sf.tag, 'Static Stability Forces')
        np.testing.assert_array_equal(sf.lift, rp.zeros((1, 1)))
        np.testing.assert_array_equal(sf.drag, rp.zeros((1, 1)))
        np.testing.assert_array_equal(sf.X, rp.zeros((1, 1)))
        np.testing.assert_array_equal(sf.Y, rp.zeros((1, 1)))
        np.testing.assert_array_equal(sf.Z, rp.zeros((1, 1)))


class TestStaticMoments(unittest.TestCase):
    def test_default_values(self):
        sm = StaticMoments()
        self.assertEqual(sm.tag, 'Static Stability Moments')
        np.testing.assert_array_equal(sm.L, rp.zeros((1, 1)))
        np.testing.assert_array_equal(sm.M, rp.zeros((1, 1)))
        np.testing.assert_array_equal(sm.N, rp.zeros((1, 1)))


class TestCoefficientDerivatives(unittest.TestCase):
    def test_default_values(self):
        cd = CoefficientDerivatives()
        self.assertEqual(cd.tag, 'Coefficient Static Stability Derivatives')
        np.testing.assert_array_equal(cd.alpha, rp.zeros((1, 1)))
        np.testing.assert_array_equal(cd.beta, rp.zeros((1, 1)))
        np.testing.assert_array_equal(cd.delta_a, rp.zeros((1, 1)))
        np.testing.assert_array_equal(cd.delta_e, rp.zeros((1, 1)))
        np.testing.assert_array_equal(cd.delta_r, rp.zeros((1, 1)))
        np.testing.assert_array_equal(cd.delta_f, rp.zeros((1, 1)))
        np.testing.assert_array_equal(cd.delta_s, rp.zeros((1, 1)))
        np.testing.assert_array_equal(cd.u, rp.zeros((1, 1)))
        np.testing.assert_array_equal(cd.v, rp.zeros((1, 1)))
        np.testing.assert_array_equal(cd.w, rp.zeros((1, 1)))
        np.testing.assert_array_equal(cd.p, rp.zeros((1, 1)))
        np.testing.assert_array_equal(cd.q, rp.zeros((1, 1)))
        np.testing.assert_array_equal(cd.r, rp.zeros((1, 1)))


class TestStaticDerivatives(unittest.TestCase):
    def test_default_values(self):
        sd = StaticDerivatives()
        self.assertEqual(sd.tag, 'Static Stability Coefficients Derivatives')
        self.assertIsInstance(sd.Clift, CoefficientDerivatives)
        self.assertIsInstance(sd.Cdrag, CoefficientDerivatives)
        self.assertIsInstance(sd.CX, CoefficientDerivatives)
        self.assertIsInstance(sd.CY, CoefficientDerivatives)
        self.assertIsInstance(sd.CZ, CoefficientDerivatives)
        self.assertIsInstance(sd.CL, CoefficientDerivatives)
        self.assertIsInstance(sd.CM, CoefficientDerivatives)
        self.assertIsInstance(sd.CN, CoefficientDerivatives)


class TestStaticStability(unittest.TestCase):
    def test_default_values(self):
        ss = StaticStability()
        self.assertEqual(ss.tag, 'Static Stability')
        self.assertIsInstance(ss.forces, StaticForces)
        self.assertIsInstance(ss.moments, StaticMoments)
        self.assertIsInstance(ss.coefficients, StaticCoefficients)
        self.assertIsInstance(ss.derivatives, StaticDerivatives)
        np.testing.assert_array_equal(ss.static_margin, rp.zeros((1, 1)))
        np.testing.assert_array_equal(ss.neutral_point, rp.zeros((1, 1)))
        np.testing.assert_array_equal(ss.spiral_criteria, rp.zeros((1, 1)))
        np.testing.assert_array_equal(ss.pitch_rate, rp.zeros((1, 1)))
        np.testing.assert_array_equal(ss.roll_rate, rp.zeros((1, 1)))
        np.testing.assert_array_equal(ss.yaw_rate, rp.zeros((1, 1)))


class TestDynamicStability(unittest.TestCase):
    def test_default_values(self):
        ds = DynamicStability()
        self.assertEqual(ds.tag, 'Dynamic Stability')
        self.assertIsInstance(ds.LongModes, Conditions)
        self.assertIsInstance(ds.LatModes, Conditions)
        self.assertEqual(ds.LongModes.tag, 'Longitudinal Modes')
        self.assertEqual(ds.LatModes.tag, 'Lateral Modes')


class TestStabilityConditions(unittest.TestCase):
    def test_default_values(self):
        sc = StabilityConditions()
        self.assertEqual(sc.tag, 'Stability')
        self.assertIsInstance(sc.static, StaticStability)
        self.assertIsInstance(sc.dynamic, DynamicStability)


if __name__ == '__main__':
    unittest.main()