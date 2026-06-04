# RCAIDE/Framework/Missions/Segments/profiles.py
# (c) Copyright 2026 Aerospace Research Community LLC
#
# Created: Mar 2026, J. Smart
# Modified: Mar 2026, J. Smart

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from typing import TYPE_CHECKING, Literal
import jax
import jax.numpy as jnp
import equinox as eqx

# --- Framework Imports (Strictly for Type Hinting to avoid Circular Imports) ---
if TYPE_CHECKING:
    from RCAIDE.Framework.State import State
    from RCAIDE.Framework.System import System
    from RCAIDE.Framework.Settings import Settings

from RCAIDE.Framework import ProcessStep
from RCAIDE.Library import Units

# ----------------------------------------------------------------------------------------------------------------------
#  Segment Profiles
# ----------------------------------------------------------------------------------------------------------------------

# Course Profiles

class ConstantCourse(ProcessStep):

    tag: str = eqx.field(static=True, default="Set Constant Course")

    true_course: float = 0.0 * Units.deg

    def __call__(self, state, system, settings):
        course_arr = jnp.full_like(state.freestream.altitude, self.true_course)
        updated_state = eqx.tree_at(lambda s: s.frames.planet.true_course, state, course_arr)

        return updated_state, system, settings

CourseProfile = ConstantCourse

# Position Profiles

class ConstantAltitude(ProcessStep):
    tag: str = eqx.field(static=True, default="Set Constant Altitude")
    altitude: float = 1.0 * Units.km
    
    def __call__(self, state, system, settings):
        # Z points down, so position vector gets negative altitude
        altitude_arr = jnp.full_like(state.freestream.altitude, self.altitude)
        updated_position = state.frames.inertial.position_vector.at[:, 2].set(-altitude_arr.flatten())
        
        updated_state = eqx.tree_at(
            lambda s: (s.freestream.altitude, s.frames.inertial.position_vector), state,
            (altitude_arr, updated_position)) 
        
        return updated_state, system, settings

class AltitudeChange(ProcessStep):
    tag: str = eqx.field(static=True, default="Set Altitude Change")
    initial_altitude: float = 1.0 * Units.km
    final_altitude: float = 10.0 * Units.km
    
    def __call__(self, state, system, settings):
        t_nondim = state.numerics.dimensionless.control_points
        altitude_profile = t_nondim * (self.final_altitude - self.initial_altitude) + self.initial_altitude
        
        updated_position = state.frames.inertial.position_vector.at[:, 2].set(-altitude_profile.flatten())

        updated_state = eqx.tree_at(
            lambda s:(s.freestream.altitude, s.frames.inertial.position_vector), state,
            (altitude_profile, updated_position))
        
        return updated_state, system, settings

PositionProfile = ConstantAltitude | AltitudeChange

# Speed Profiles
# TODO: Add sideslip calculation and/or deprecate in favor of full 6-DOF

class ConstantSpeed(ProcessStep):
    tag: str = eqx.field(static=True, default="Set Constant Speed")
    speed: float = 1.0 * Units.m/Units.s

    def __call__(self, state, system, settings):
        new_speed = jnp.full_like(state.freestream.speed, self.speed)
        
        # Set the X-component of the inertial velocity vector
        new_velocity = state.frames.inertial.velocity_vector.at[:, 0].set(new_speed.flatten())
        
        updated_state = eqx.tree_at(
            lambda s: (s.freestream.speed, s.frames.inertial.velocity_vector), 
            state, 
            (new_speed, new_velocity)
        )
        return updated_state, system, settings

class ConstantMach(ProcessStep):
    tag: str = eqx.field(static=True, default="Set Constant Mach Number")

    mach_number: float = 0.5

    def __call__(self, state, system, settings):
        alt = state.freestream.altitude
        T = state.freestream.atmosphere.compute_temperatue(alt)
        a = state.freestream.atmosphere.gas.compute_speed_of_sound(T)
        
        v_mag = self.mach_number * a

        new_velocity = state.frames.inertial.velocity_vector.at[:, 0].set(v_mag.flatten())
        
        updated_state = eqx.tree_at(
            lambda s: (s.freestream.speed, s.frames.inertial.velocity_vector), 
            state, 
            (v_mag, new_velocity)
        )
        return updated_state, system, settings

SpeedProfile = ConstantSpeed | ConstantMach

# Velocity Profiles

class ConstantAltitudeChangeRate(ProcessStep):
    tag: str = eqx.field(static=True, default="Set Constant Alt. Change Rate")
    
    change_rate: float = 0.0 * Units.m/Units.s

    def __call__(self, state, system, settings):
        v_mag = state.freestream.speed
        v_z = -self.change_rate # Z points down, so positive rate (climb) is negative and vice-versa
        v_x = jnp.sqrt(v_mag **2 - v_z ** 2)
        
        updated_velocity = state.frames.inertial.velocity_vector.at[:, 0].set(v_x.squeeze(-1))
        updated_velocity = updated_velocity.at[:, 2].set(v_z)
        
        updated_state = eqx.tree_at(lambda s:s.frames.inertial.velocity_vector, state, updated_velocity)
        return updated_state, system, settings


VelocityProfile = ConstantAltitudeChangeRate

# Duration Profiles

class FixedDistance(ProcessStep):
    tag: str = eqx.field(static=True, default="Set Fixed Distance Duration")
    distance: float = 1.0 * Units.km

    def __call__(self, state, system, settings):
        v_avg   = jnp.linalg.norm(jnp.average(state.frames.inertial.velocity_vector, axis=0))

        t_0 = state.frames.inertial.time[0, 0]
        t_f = t_0 + self.distance / v_avg

        t_nondim = state.numerics.dimensionless.control_points
        time = t_nondim * (t_f - t_0) + t_0

        updated_state = eqx.tree_at(lambda s:s.frames.inertial.time, state, time)

        return updated_state, system, settings

class FixedTime(ProcessStep):
    tag: str = eqx.field(static=True, default="Set Fixed Time Duration")
    time: float = 1.0 * Units.s

    def __call__(self, state, system, settings):
        t_0 = state.frames.inertial.time[0, 0]
        t_f = t_0 + self.time
        
        t_nondim = state.numerics.dimensionless.control_points
        time = t_nondim * (t_f - t_0) + t_0

        updated_state = eqx.tree_at(lambda s:s.frames.inertial.time, state, time)

        return updated_state, system, settings

DurationProfile = FixedDistance | FixedTime
