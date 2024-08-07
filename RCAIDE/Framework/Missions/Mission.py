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
from RCAIDE.Framework.Missions.Initialization import *

# ----------------------------------------------------------------------------------------------------------------------
# Mission Segment
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class MissionInitialization(Process):

    name: str = 'Mission Initialization'

    def __post_init__(self):

        self.append(ProcessStep(name="Initialize Time",
                                function=initialize_time))
        self.append(ProcessStep(name="Initialize Mass",
                                function=initialize_mass))
        self.append(ProcessStep(name="Initialize Energy",
                                function=initialize_energy))


@dataclass(kw_only=True)
class MissionIteration(Process):

    name: str = "Mission Iteration"

    def __post_init__(self):
        return

@dataclass(kw_only=True)
class MissionFinalization(Process):

    name: str = "Mission Finalization"


@dataclass(kw_only=True)
class MissionSegment(Process):

    name: str = "Mission Segment"

    analyses: list[Process] = field(default_factory=list)

    initialization: MissionInitialization   = MissionInitialization()
    iteration:      MissionIteration        = MissionIteration()
    finalization:   MissionFinalization     = MissionFinalization()

    def __post_init__(self):
        self.append(ProcessStep(name="Expand State",
                                function=expand_state))

        self.append(self.initialization)
        self.append(self.iteration)
        self.append(self.finalization)



