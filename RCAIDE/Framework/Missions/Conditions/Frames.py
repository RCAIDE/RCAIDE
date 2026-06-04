# RCAIDE/Framework/Missions/Conditions/Frames.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------



# package imports
import equinox as eqx
import jax.numpy as jnp

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Frames
# ----------------------------------------------------------------------------------------------------------------------

class Frame(Conditions):

    # Attribute             Type        Default Value
    tag:                    str         = eqx.field(static=True, default='Frame')
    
    transform_to_inertial:  jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty((0, 3)))

    total_force_vector:     jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty((0, 3)))
    total_moment_vector:    jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty((0, 3)))


class InertialFrame(Frame):

    # Attribute                     Type        Default Value
    tag:                            str         = eqx.field(static=True, default='Inertial Frame')

    position_vector:                jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty((0, 3)))

    velocity_vector:                jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty((0, 3)))
    acceleration_vector:            jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty((0, 3)))

    angular_velocity_vector:        jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty((0, 3)))
    angular_acceleration_vector:    jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty((0, 3)))

    gravity_force_vector:           jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty((0, 3)))

    time:                           jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty((0)))
    system_range:                   jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty((0)))


class BodyFrame(Frame):

    # Attribute             Type        Default Value
    tag:                    str         = eqx.field(static=True, default='Body Frame')

    inertial_rotations:     jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty((0, 3)))
    thrust_force_vector:    jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty((0, 3)))
    moment_vector:          jnp.ndarray  = eqx.field(default_factory=lambda: jnp.empty((0, 3)))

class WindFrame(Frame):

    # Attribute         Type            Default Value
    tag:                str             = eqx.field(static=True, default='Wind Frame')

    body_rotations:     jnp.ndarray      = eqx.field(default_factory=lambda: jnp.empty((0, 3)))
    transform_to_body:  jnp.ndarray      = eqx.field(default_factory=lambda: jnp.empty((0, 3)))

    velocity_vector:    jnp.ndarray      = eqx.field(default_factory=lambda: jnp.empty((0, 3)))
    force_vector:       jnp.ndarray      = eqx.field(default_factory=lambda: jnp.empty((0, 3)))
    moment_vector:      jnp.ndarray      = eqx.field(default_factory=lambda: jnp.empty((0, 3)))


class PlanetFrame(Frame):

    # Attribute     Type            Default Value
    tag:            str             = eqx.field(static=True, default='Planet Frame')
    start_time:     jnp.ndarray     = eqx.field(default_factory=lambda: jnp.empty(0))

    # Default to takeoff at JFK
    latitude:       jnp.ndarray     = eqx.field(default_factory=lambda: jnp.array([40.6446]))
    longitude:      jnp.ndarray     = eqx.field(default_factory=lambda: jnp.array([73.7797]))

    true_course:    jnp.ndarray     = eqx.field(default_factory=lambda: jnp.empty(0))


class FrameConditions(Conditions):

    # Attribute     Type            Default Value
    tag:            str             = eqx.field(static=True, default='Dynamic Frames')

    inertial:       InertialFrame   = eqx.field(default_factory=InertialFrame)
    body:           BodyFrame       = eqx.field(default_factory=BodyFrame)
    wind:           WindFrame       = eqx.field(default_factory=WindFrame)
    planet:         PlanetFrame     = eqx.field(default_factory=PlanetFrame)
