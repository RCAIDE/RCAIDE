# RCAIDE/Framework/Missions/Mission.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from typing import Callable
from dataclasses import dataclass, field

# package imports

from scipy.optimize import fsolve

# RCAIDE imports

from RCAIDE.Framework import Process, ProcessStep
from RCAIDE.Framework.Missions.Initialization   import *
from RCAIDE.Framework.Missions.Update           import *

# ----------------------------------------------------------------------------------------------------------------------
# Mission Segment
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class SegmentInitialization(Process):

    name: str = 'Segment Initialization'

    def __post_init__(self):

        default_steps = [
            #Step Name                          Step Functions
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
            ("Update Altitude",             update_),
            ("Update Atmosphere",           update_),
            ("Update Gravity",              update_),
            ("Update Freestream",           update_),
            ("Update Orientations",         update_),
            ("Update Energy",               update_),
            ("Update Aerodynamics",         update_),
            ("Update Stability",            update_),
            ("Update Mass",                 update_),
            ("Update Forces",               update_),
            ("Update Moments",              update_),
            ("Update Planetary Position",   update_)
        ]

        for name, function in default_steps:
            self.append(ProcessStep(name=name, function=function))


@dataclass(kw_only=True)
class SegmentConvergence(Process):

    name: str = "Segment Convergence"


@dataclass(kw_only=True)
class SegmentFinalization(Process):

    name: str = "Mission Finalization"


@dataclass(kw_only=True)
class MissionSegment(Process):

    name: str = "Mission Segment"

    analyses: list[Process] = field(default_factory=list)

    initialization: SegmentInitialization   = SegmentInitialization()
    iteration:      SegmentUpdate           = SegmentUpdate()
    finalization:   SegmentFinalization     = SegmentFinalization()

    def __post_init__(self):
        self.append(ProcessStep(name="Expand State",
                                function=expand_state))

        self.append(self.initialization)
        self.append(self.iteration)
        self.append(self.finalization)



