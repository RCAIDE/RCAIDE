# RCAIDE/Framework/Missions/Conditions/Stability.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  Import
# ----------------------------------------------------------------------------------------------------------------------


# package imports
import equinox as eqx
import jax.numpy as jnp

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Stability
# ----------------------------------------------------------------------------------------------------------------------


class StaticCoefficients(Conditions):
    """
    Static stability coefficients for an aircraft.

    This class encapsulates various aerodynamic coefficients and forces
    relevant to the static stability analysis of an aircraft.

    Attributes
    ----------
    name : str
        The name of the coefficient set.
    lift : jnp.ndarray
        The lift coefficient. Shape: (1, 1)
    drag : jnp.ndarray
        The drag coefficient. Shape: (1, 1)
    X : jnp.ndarray
        The X-axis force coefficient. Shape: (1, 1)
    Y : jnp.ndarray
        The Y-axis force coefficient. Shape: (1, 1)
    Z : jnp.ndarray
        The Z-axis force coefficient. Shape: (1, 1)
    L : jnp.ndarray
        The rolling moment coefficient. Shape: (1, 1)
    M : jnp.ndarray
        The pitching moment coefficient. Shape: (1, 1)
    N : jnp.ndarray
        The yawing moment coefficient. Shape: (1, 1)
    e : jnp.ndarray
        The Oswald efficiency factor. Shape: (1, 1)

    Notes
    -----
    All coefficient arrays are initialized as 1x1 numpy arrays with zero values.
    These can be updated with actual coefficient values during analysis.
    """

    # Attribute     Type        Default Value
    tag:            str         = eqx.field(static=True, default='Static Stability Coefficients')

    lift:           jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))
    drag:           jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))

    X:              jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))
    Y:              jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))
    Z:              jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))

    L:              jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))
    M:              jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))
    N:              jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))

    e:              jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))



class StaticForces(Conditions):
    """
    Static forces acting on an aircraft.

    This class encapsulates the static forces that are relevant to aircraft 
    stability analysis, including lift, drag, and forces in the X, Y, and Z directions.

    Attributes
    ----------
    name : str
        The name of the static forces set. Default is 'Static Stability Forces'.
    lift : jnp.ndarray
        The lift force. Shape: (1, 1)
    drag : jnp.ndarray
        The drag force. Shape: (1, 1)
    X : jnp.ndarray
        The force in the X-direction. Shape: (1, 1)
    Y : jnp.ndarray
        The force in the Y-direction. Shape: (1, 1)
    Z : jnp.ndarray
        The force in the Z-direction. Shape: (1, 1)

    Notes
    -----
    All force arrays are initialized as 1x1 numpy arrays with zero values.
    These can be updated with actual force values during analysis.
    """

    # Attribute     Type        Default Value
    tag:           str         = eqx.field(static=True, default='Static Stability Forces')

    lift:           jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty(0))
    drag:           jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty(0))

    X:              jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty(0))
    Y:              jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty(0))
    Z:              jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty(0))



class StaticMoments(Conditions):
    """
    Represents the static moments acting on an aircraft.

    This class encapsulates the static moments that are relevant to aircraft 
    stability analysis, including rolling, pitching, and yawing moments.

    Attributes
    ----------
    name : str
        The name of the static moments set. Default is 'Static Stability Moments'.
    L : jnp.ndarray
        The rolling moment. Shape: (1, 1)
    M : jnp.ndarray
        The pitching moment. Shape: (1, 1)
    N : jnp.ndarray
        The yawing moment. Shape: (1, 1)

    Notes
    -----
    All moment arrays are initialized as 1x1 numpy arrays with zero values.
    These can be updated with actual moment values during analysis.
    """

    # Attribute     Type        Default Value
    tag:            str         = eqx.field(static=True, default='Static Stability Moments')

    L:              jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty(0))
    M:              jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty(0))
    N:              jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty(0))



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
    
    alpha : jnp.ndarray
        Derivative with respect to angle of attack. Shape: (1, 1)
    beta : jnp.ndarray
        Derivative with respect to sideslip angle. Shape: (1, 1)
    
    delta_a : jnp.ndarray
        Derivative with respect to aileron deflection. Shape: (1, 1)
    delta_e : jnp.ndarray
        Derivative with respect to elevator deflection. Shape: (1, 1)
    delta_r : jnp.ndarray
        Derivative with respect to rudder deflection. Shape: (1, 1)
    delta_f : jnp.ndarray
        Derivative with respect to flap deflection. Shape: (1, 1)
    delta_s : jnp.ndarray
        Derivative with respect to spoiler deflection. Shape: (1, 1)
    
    u : jnp.ndarray
        Derivative with respect to forward velocity. Shape: (1, 1)
    v : jnp.ndarray
        Derivative with respect to lateral velocity. Shape: (1, 1)
    w : jnp.ndarray
        Derivative with respect to vertical velocity. Shape: (1, 1)
    
    p : jnp.ndarray
        Derivative with respect to roll rate. Shape: (1, 1)
    q : jnp.ndarray
        Derivative with respect to pitch rate. Shape: (1, 1)
    r : jnp.ndarray
        Derivative with respect to yaw rate. Shape: (1, 1)

    Notes:
    -----
    All derivative arrays are initialized as 1x1 numpy arrays with zero values.
    These can be updated with actual derivative values during analysis.
    """

    # Attribute     Type        Default Value
    tag:            str         = eqx.field(static=True, default='Coefficient Static Stability Derivatives')

    # Throttle Derivative
    throttle:       jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))

    # Stability Axis Derivatives
    beta:           jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))
    alpha:          jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))

    delta_a:        jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))
    delta_e:        jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))
    delta_r:        jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))
    delta_f:        jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))
    delta_s:        jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))

    # Body Axis Derivatives

    u:              jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))
    v:              jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))
    w:              jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))

    p:              jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))
    q:              jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))
    r:              jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))



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

    # Attribute     Type            Default Value
    tag:            str             = eqx.field(static=True, default='Static Stability Coefficients Derivatives')

    Clift:  CoefficientDerivatives  = eqx.field(default_factory=lambda:
                                            CoefficientDerivatives(tag='Lift Coefficient Static Stability Derivatives'))
    Cdrag:  CoefficientDerivatives  = eqx.field(default_factory=lambda:
                                            CoefficientDerivatives(tag='Drag Coefficient Static Stability Derivatives'))

    CX:     CoefficientDerivatives  = eqx.field(default_factory=lambda:
                                            CoefficientDerivatives(tag='X Coefficient Static Stability Derivatives'))
    CY:     CoefficientDerivatives  = eqx.field(default_factory=lambda:
                                            CoefficientDerivatives(tag='Y Coefficient Static Stability Derivatives'))
    CZ:     CoefficientDerivatives  = eqx.field(default_factory=lambda:
                                            CoefficientDerivatives(tag='Z Coefficient Static Stability Derivatives'))

    CL:     CoefficientDerivatives  = eqx.field(default_factory=lambda:
                                            CoefficientDerivatives(tag='L Coefficient Static Stability Derivatives'))
    CM:     CoefficientDerivatives  = eqx.field(default_factory=lambda:
                                            CoefficientDerivatives(tag='M Coefficient Static Stability Derivatives'))
    CN:     CoefficientDerivatives  = eqx.field(default_factory=lambda:
                                            CoefficientDerivatives(tag='N Coefficient Static Stability Derivatives'))



class StaticStability(Conditions):

    tag:                str                 = eqx.field(static=True, default='Static Stability')
    
    forces:             StaticForces        = eqx.field(default_factory=StaticForces)
    moments:            StaticMoments       = eqx.field(default_factory=StaticMoments)
    
    coefficients:       StaticCoefficients  = eqx.field(default_factory=StaticCoefficients)
    derivatives:        StaticDerivatives   = eqx.field(default_factory=StaticDerivatives)
    
    static_margin:      jnp.ndarray         = eqx.field(default_factory=lambda: jnp.empty(0))
    neutral_point:      jnp.ndarray         = eqx.field(default_factory=lambda: jnp.empty(0))
    spiral_criteria:    jnp.ndarray         = eqx.field(default_factory=lambda: jnp.empty(0))
    
    pitch_rate:         jnp.ndarray         = eqx.field(default_factory=lambda: jnp.empty(0))
    roll_rate:          jnp.ndarray         = eqx.field(default_factory=lambda: jnp.empty(0))
    yaw_rate:           jnp.ndarray         = eqx.field(default_factory=lambda: jnp.empty(0))



class DynamicStability(Conditions):

    #Attribute      Type        Default Value
    tag:            str         = eqx.field(static=True, default='Dynamic Stability')

    LongModes:      Conditions  = eqx.field(default_factory=lambda: Conditions(tag='Longitudinal Modes'))
    LatModes:       Conditions  = eqx.field(default_factory=lambda: Conditions(tag='Lateral Modes'))




class StabilityConditions(Conditions):

    # Attribute     Type                Default Value
    tag:            str                 = eqx.field(static=True, default='Stability')

    static:         StaticStability     = eqx.field(default_factory=StaticStability)
    dynamic:        DynamicStability    = eqx.field(default_factory=DynamicStability)