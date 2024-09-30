# RCAIDE/Framework/Missions/Conditions/Stability.py
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
from RCAIDE.Framework.Missions.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Stability
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class StaticCoefficients(Conditions):

    # Attribute     Type        Default Value
    name:           str         = 'Static Stability Coefficients'

    lift:           np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    drag:           np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    X:              np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    Y:              np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    Z:              np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    L:              np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    M:              np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    N:              np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    e:              np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))


@dataclass(kw_only=True)
class StaticForces(Conditions):

    # Attribute     Type        Default Value
    name:           str         = 'Static Stability Forces'

    lift:           np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    drag:           np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    X:              np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    Y:              np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    Z:              np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))


@dataclass(kw_only=True)
class StaticMoments(Conditions):

    # Attribute     Type        Default Value
    name:           str         = 'Static Stability Moments'

    L:              np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    M:              np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    N:              np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))


@dataclass(kw_only=True)
class CoefficientDerivatives(Conditions):

    # Attribute     Type        Default Value
    name:           str         = 'Coefficient Static Stability Derivatives'

    # Stability Axis Derivatives
    alpha:          np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    beta:           np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    delta_a:        np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    delta_e:        np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    delta_r:        np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    delta_f:        np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    delta_s:        np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    # Body Axis Derivatives

    u:              np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    v:              np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    w:              np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    p:              np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    q:              np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    r:              np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))


@dataclass(kw_only=True)
class StaticDerivatives(Conditions):

    # Attribute     Type        Default Value
    name:           str         = 'Static Stability Coefficients Derivatives'

    Clift:  CoefficientDerivatives = field(default_factory=lambda:
                                           CoefficientDerivatives(name='Lift Coefficient Static Stability Derivatives'))
    Cdrag:  CoefficientDerivatives = field(default_factory=lambda:
                                           CoefficientDerivatives(name='Drag Coefficient Static Stability Derivatives'))

    CX:     CoefficientDerivatives = field(default_factory=lambda:
                                           CoefficientDerivatives(name='X Coefficient Static Stability Derivatives'))
    CY:     CoefficientDerivatives = field(default_factory=lambda:
                                           CoefficientDerivatives(name='Y Coefficient Static Stability Derivatives'))
    CZ:     CoefficientDerivatives = field(default_factory=lambda:
                                           CoefficientDerivatives(name='Z Coefficient Static Stability Derivatives'))

    CL:     CoefficientDerivatives = field(default_factory=lambda:
                                           CoefficientDerivatives(name='L Coefficient Static Stability Derivatives'))
    CM:     CoefficientDerivatives = field(default_factory=lambda:
                                           CoefficientDerivatives(name='M Coefficient Static Stability Derivatives'))
    CN:     CoefficientDerivatives = field(default_factory=lambda:
                                           CoefficientDerivatives(name='N Coefficient Static Stability Derivatives'))


@dataclass(kw_only=True)
class StaticStability(Conditions):

    #Attribute          Type                Default Value
    name:               str                 = 'Static Stability'

    forces:             StaticForces        = field(default_factory=lambda: StaticForces())
    moments:            StaticMoments       = field(default_factory=lambda: StaticMoments())

    coefficients:       StaticCoefficients  = field(default_factory=lambda: StaticCoefficients())
    derivatives:        StaticDerivatives   = field(default_factory=lambda: StaticDerivatives())

    static_margin:      np.ndarray          = field(default_factory=lambda: np.zeros((1, 1)))
    neutral_point:      np.ndarray          = field(default_factory=lambda: np.zeros((1, 1)))
    spiral_criteria:    np.ndarray          = field(default_factory=lambda: np.zeros((1, 1)))

    pitch_rate:         np.ndarray          = field(default_factory=lambda: np.zeros((1, 1)))
    roll_rate:          np.ndarray          = field(default_factory=lambda: np.zeros((1, 1)))
    yaw_rate:           np.ndarray          = field(default_factory=lambda: np.zeros((1, 1)))


@dataclass(kw_only=True)
class DynamicStability(Conditions):

    #Attribute      Type        Default Value
    name:           str         = 'Dynamic Stability'

    LongModes:      Conditions  = field(default_factory=lambda: Conditions(name='Longitudinal Modes'))
    LatModes:       Conditions  = field(default_factory=lambda: Conditions(name='Lateral Modes'))



@dataclass(kw_only=True)
class StabilityConditions(Conditions):

    # Attribute     Type                Default Value
    name:           str                 = 'Stability'

    static:         StaticStability     = StaticStability()
    dynamic:        DynamicStability    = DynamicStability()
