# $NAME.py
# (c) Copyright 2025 Aerospace Research Community LLC
#
# Created: Oct 2025, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import chex
import RNUMPY as rp

import RCAIDE.Framework as rcf

from RCAIDE.Framework import ProcessStep
from RCAIDE.Framework.Missions.Segments import Segment
from RCAIDE.Framework.Missions.Conditions.Controls import DirectControlVariable

# ----------------------------------------------------------------------------------------------------------------------
#  Cruise
# ----------------------------------------------------------------------------------------------------------------------


@chex.dataclass(kw_only=True)
class Cruise(Segment):

    tag: str = 'Cruise'

    distance: float = 0.0
    true_course: float = 0.0

    def __post_init__(self):
        super(Cruise, self).__post_init__()


@chex.dataclass(kw_only=True)
class TestCSACruise(Cruise):

    tag: str = 'Constant Speed & Altitude Cruise'

    altitude: float = None
    air_speed: float = None

    active_controls: tuple[str|DirectControlVariable, ...] = None
    active_residuals: tuple[str|DirectControlVariable, ...] = ('Force X', 'Force Z')

    def initialize_dynamics(
            self,
            state: "rcf.State",
            system: "rcf.System",
            settings: "rcf.Settings",
    ):

        alt = self.altitude
        xf = self.distance
        av = self.air_speed
        beta = self.sideslip_angle

        if not self.air_speed:
            av = rp.linalg.norm(state.frames.inertial.velocity_vector[-1])
        if not self.altitude:
            alt = -1.0 * state.frames.inertial.position_vector[-1, 2]

        v_x = rp.cos(beta) * av
        v_y = rp.sin(beta) * av
        t_0 = state.frames.inertial.time[0, 0]
        t_f = t_0 + xf / av

        t_nondim = state.numerics.dimensionless.control_points
        time = t_nondim * (t_f - t_0) + t_0

        state.freestream.altitude =state.freestream.altitude.at[:, 0].set(alt)
        state.frames.inertial.position_vector = state.frames.inertial.position_vector.at[:, 2].set(-alt)
        state.frames.inertial.velocity_vector = state.frames.inertial.velocity_vector.at[:, 0].set(v_x)
        state.frames.inertial.velocity_vector = state.frames.inertial.velocity_vector.at[:, 1].set(v_y)
        state.frames.inertial.time = time

        # Set active controls and dynamics
        return state, system, settings

    def __post_init__(self):

        lift_control = DirectControlVariable(tag='Lift Coefficient',
                                             path=("aerodynamics", "coefficients", "lift", "total"),
                                             path_indices=(slice(None), 0),
                                             active=True
                                             )
        drag_control = DirectControlVariable(tag='Drag Coefficient',
                                             path=("aerodynamics", "coefficients", "drag", "total"),
                                             path_indices=(slice(None), 0),
                                             active=True
                                             )

        self.active_controls = lift_control, drag_control
        self.controls_initial_guess = (1.0, 0.05)

        self.initialize.append(ProcessStep(tag='Dynamics and Controls',
                                           function=self.initialize_dynamics))

        super(TestCSACruise, self).__post_init__()