# RCAIDE/Framework/Missions/Conditions/Aerodynamics.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# package imports
import equinox as eqx
import jax.numpy as jnp

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Aerodynamics
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------
#  Coefficients
# ----------------------------------------------------------

# Component-Level Bookkeeping ------------------------------

class ComponentCoefficients(Conditions):
    tag:            str = eqx.field(static=True, default='Component Coefficients')

    total:          jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty(0))

    # Component Arrays: (n_time, n_components)
    wings:          jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty((0, 0)))
    fuselages:      jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty((0, 0)))
    nacelles:       jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty((0, 0)))

# Lift Coefficients ----------------------------------------

class LiftCoefficients(Conditions):

    # Attribute     Type            Default Value
    tag:            str             = eqx.field(static=True, default='Lift Coefficients')

    total:          jnp.ndarray     = eqx.field(default_factory=lambda: jnp.empty(0))

    inviscid:       ComponentCoefficients   = eqx.field(default_factory=lambda: ComponentCoefficients(tag='Inviscid Lift'))
    compressible:   ComponentCoefficients   = eqx.field(default_factory=lambda: ComponentCoefficients(tag='Compressible Lift'))

# Drag Coefficients ----------------------------------------

class InducedDrag(Conditions):

    # Attribute   Type            Default Value
    tag:          str             = eqx.field(static=True, default='Induced Drag')

    total:        jnp.ndarray     = eqx.field(default_factory=lambda: jnp.empty(0))

    inviscid:     ComponentCoefficients = eqx.field(default_factory=lambda: ComponentCoefficients(tag='Inviscid Induced Drag'))
    viscous:      ComponentCoefficients = eqx.field(default_factory=lambda: ComponentCoefficients(tag='Viscous Induced Drag'))
    near_field:   ComponentCoefficients = eqx.field(default_factory=lambda: ComponentCoefficients(tag='Near-Field Induced Drag'))
    far_field:    ComponentCoefficients = eqx.field(default_factory=lambda: ComponentCoefficients(tag='Far-Field Induced Drag'))


class DragCoefficients(Conditions):

    # Attribute     Type            Default Value
    tag:            str             = eqx.field(static=True, default='Drag Coefficients')

    total:          jnp.ndarray     = eqx.field(default_factory=lambda: jnp.empty(0))

    parasite:       ComponentCoefficients = eqx.field(default_factory=lambda: ComponentCoefficients(tag='Parasite Drag'))
    compressible:   ComponentCoefficients = eqx.field(default_factory=lambda: ComponentCoefficients(tag='Compressible Drag'))
    miscellaneous:  ComponentCoefficients = eqx.field(default_factory=lambda: ComponentCoefficients(tag='Miscellaneous Drag'))
    spoiler:        ComponentCoefficients = eqx.field(default_factory=lambda: ComponentCoefficients(tag='Spoiler Drag'))

    induced:        InducedDrag = eqx.field(default_factory=InducedDrag)

# Moment Coefficients --------------------------------------

class MomentCoefficients(Conditions):

    # Attribute         Type            Default Value
    tag:                str             = eqx.field(static=True, default='Moment Coefficients')

    pitch:              jnp.ndarray     = eqx.field(default_factory=lambda: jnp.empty(0))
    roll:               jnp.ndarray     = eqx.field(default_factory=lambda: jnp.empty(0))
    yaw:                jnp.ndarray     = eqx.field(default_factory=lambda: jnp.empty(0))

# All Coefficients -----------------------------------------

class AerodynamicCoefficients(Conditions):

    # Attribute         Type                Default Value
    tag:                str                 = eqx.field(static=True, default='Aerodynamic Coefficients')

    lift:               LiftCoefficients    = eqx.field(default_factory=LiftCoefficients)
    drag:               DragCoefficients    = eqx.field(default_factory=DragCoefficients)
    
    moments:            MomentCoefficients  = eqx.field(default_factory=MomentCoefficients)

    X:                  jnp.ndarray         = eqx.field(default_factory=lambda: jnp.empty(0))
    Y:                  jnp.ndarray         = eqx.field(default_factory=lambda: jnp.empty(0))
    Z:                  jnp.ndarray         = eqx.field(default_factory=lambda: jnp.empty(0))

# ----------------------------------------------------------
#  Aerodynamic Angles
# ----------------------------------------------------------

class AerodynamicAngles(Conditions):

    # Attribute         Type        Default Value
    tag:                str         = eqx.field(static=True, default='Aerodynamic Angles')

    alpha:              jnp.ndarray      = eqx.field(default_factory=lambda: jnp.empty(0)) # Y-axis / angle of attack
    beta:               jnp.ndarray      = eqx.field(default_factory=lambda: jnp.empty(0)) # Z-axis / sideslip angle
    phi:                jnp.ndarray      = eqx.field(default_factory=lambda: jnp.empty(0)) # X-axis / roll angle

# ----------------------------------------------------------
#  Full Aerodynamic Conditions
# ----------------------------------------------------------


class AerodynamicsConditions(Conditions):

    # Attribute     Type                    Default Value
    tag:            str                     = eqx.field(static=True, default='Aerodynamics')

    angles:         AerodynamicAngles       = eqx.field(default_factory=AerodynamicAngles)

    coefficients:   AerodynamicCoefficients = eqx.field(default_factory=AerodynamicCoefficients)
