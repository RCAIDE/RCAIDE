# RCAIDE/Framework/Missions/Segments/Climb.py
# (c) Copyright 2025 Aerospace Research Community LLC
#
# Created: Sep, 2025, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT 
# ----------------------------------------------------------------------------------------------------------------------

import chex
import RNUMPY as rp

import RCAIDE.Framework as rcf

from RCAIDE.Framework import ProcessStep
from RCAIDE.Framework.Missions.Segments import Segment
from RCAIDE.Framework.Missions.Initialize import initialize_altitude_differential

# ----------------------------------------------------------------------------------------------------------------------
# Climb
# ----------------------------------------------------------------------------------------------------------------------


@chex.dataclass(kw_only=True)
class AltitudeChange(Segment):

    tag: str = 'Altitude Change'

    altitude_start: float = None
    altitude_end:   float = 0.0

    def __post_init__(self):
        super(AltitudeChange, self).__post_init__()

        self.initialize.append(
            ProcessStep(tag='Altitude Differential',
                        function=initialize_altitude_differential)
        )


@chex.dataclass(kw_only=True)
class CSRAltitudeChange(AltitudeChange):

    tag: str = 'Constant Speed & Rate Altitude Change'

    rate:           float = 0.0
    air_speed:      float = None
    true_course:    float = 0.0

    active_controls = ("body_angle", "throttle")
    active_residuals = ("force_x", "force_z")

    def initialize_conditions(
            self,
            state: "rcf.State",
            system: "rcf.System",
            settings: "rcf.Settings",
    ):
        # Unpack inputs from segment parameters and state

        rate    = self.rate
        av      = self.air_speed

        alt0    = self.altitude_start
        altf    = self.altitude_end

        beta    = self.sideslip_angle

        t_nondim = state.numerics.dimensionless.control_points

        # If air speed and altitude are not provided, inherit from previous segment

        if not self.air_speed:
            av = rp.linalg.norm(state.frames.inertial.velocity_vector[-1])
        if not self.altitude_start:
            alt0 = -1.0 * state.frames.inertial.position_vector[-1, 2]

        # Calculate velocity vector in inertial frame
        v_xy    = rp.sqrt(av ** 2 - rate ** 2)
        v_x     = rp.cos(beta) * v_xy
        v_y     = rp.sin(beta) * v_xy

        state.frames.inertial.velocity_vector[:, 0] = v_x
        state.frames.inertial.velocity_vector[:, 1] = v_y
        state.frames.inertial.velocity_vector[:, 2] = -rate

        # Calculate altitude using time discretization
        alt = t_nondim * (altf - alt0) + alt0
        state.frames.inertial.position_vector[:, 2] = -alt[:, 0]
        state.freestream.altitude[:, 0] = alt[:, 0]

        return state, system, settings


    def __post_init__(self):
        super(CSRAltitudeChange, self).__post_init__()
        self.initialize.append(
            ProcessStep(tag='Conditions',
                        function=self.initialize_conditions)
        )
