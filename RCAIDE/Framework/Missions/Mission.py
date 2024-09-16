# RCAIDE/Framework/Missions/Mission.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from typing import Callable, List, Any, Tuple
from dataclasses import dataclass, field

# package imports

import numpy as np
from scipy.optimize import fsolve

# RCAIDE imports

import RCAIDE.Framework as rcf
from RCAIDE.Framework import Process, ProcessStep
from RCAIDE.Framework.Process import skip
from RCAIDE.Framework.Missions.Conditions   import Conditions
from RCAIDE.Framework.Missions.Initialize   import *
from RCAIDE.Framework.Missions.Update       import *

# ----------------------------------------------------------------------------------------------------------------------
# Mission Segment
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class SegmentInitialization(Process):

    name: str = 'Segment Initialization'

    def __post_init__(self):

        default_steps = [
            # Step Name                         Step Functions
            ("Expand State",                    expand_state),
            ("Initialize Time",                 initialize_time),
            ("Initialize Mass",                 initialize_mass),
            ("Initialize Energy",               initialize_energy),
            ("Initialize Inertial Position",    initialize_inertial_position),
            ("Initialize Planetary Position",   initialize_planetary_position)
        ]

        for name, function in default_steps:
            self.append(ProcessStep(name=name, function=function))


@dataclass(kw_only=True)
class SegmentUpdate(Process):

    name: str = "Segment Iteration"

    def __post_init__(self):

        default_steps = [
            ("Update Time Differentials",   update_time_differentials),
            ("Update Acceleration",         update_acceleration),
            ("Update Angular Acceleration", update_angular_acceleration),
            ("Update Altitude",             update_altitude),
            ("Update Atmosphere", skip),
            ("Update Gravity", skip),
            ("Update Freestream",           update_freestream),
            ("Update Orientations",         update_orientations),
            ("Update Energy", skip),
            ("Update Aerodynamics", skip),
            ("Update Stability", skip),
            ("Update Mass", skip),
            ("Update Forces",               update_forces),
            ("Update Moments",              update_moments),
            ("Update Planetary Position", skip)
        ]

        for name, function in default_steps:
            self.append(ProcessStep(name=name, function=function))


@dataclass(kw_only=True)
class SegmentConvergence(Process):

    name: str = "Segment Convergence"

    calculate_residuals:    Callable = None

    root_finder_args:       List = field(default_factory=list)
    root_finder_kwargs:     dict = None
    results_parser:         Callable[[Any], Tuple[rcf.State, rcf.Settings, rcf.System]] = skip

    initial_unknowns:       np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    # Special override of process call to handle root finding, still follows process type flow
    def __call__(self,
                 State: rcf.State,
                 Settings: rcf.Settings,
                 System: rcf.System) -> Tuple[rcf.State, rcf.Settings, rcf.System]:

        # Converge root of residuals

        root_finder = Settings.root_finder

        if self.root_finder_kwargs is None:
            # Assume fsolve is the default root finder and that the calculate_residuals function is provided
            self.root_finder_kwargs = {
                'func': self.calculate_residuals,
                'x0': State.unknowns.pack_array(),
                'args': (State, Settings, System),
                'xtol': State.numerics.solution_tolerance,
                'maxfev': State.numerics.max_evaluations,
                'epsfcn': State.numerics.step_size,
                'full_output': True
            }

        results = root_finder(*self.root_finder_args, **self.root_finder_kwargs)

        return self.results_parser(results)


@dataclass(kw_only=True)
class SegmentFinalization(Process):

    name: str = "Mission Finalization"


@dataclass(kw_only=True)
class MissionSegment(Process):

    # Attribute             Type                    Default Value
    name:                   str                     = "Mission Segment"

    analyses:               list[Process]           = field(default_factory=list)

    initialize:             SegmentInitialization   = SegmentInitialization()
    update:                 SegmentUpdate           = SegmentUpdate()
    converge:               SegmentConvergence      = SegmentConvergence()
    finalize:               SegmentFinalization     = SegmentFinalization()

    def __post_init__(self):

        for analysis in self.analyses:
            self.update.append(analysis)

        self.append(self.initialize)
        self.append(self.converge)
        self.append(self.update)
        self.append(self.finalize)


if __name__ == '__main__':
    seg = MissionSegment()
    print(seg.details)
    print('Done')
