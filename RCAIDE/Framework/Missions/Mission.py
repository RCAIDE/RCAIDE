# RCAIDE/Framework/Missions/Mission.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field

# RCAIDE Imports

from RCAIDE.Framework import State, Settings, System, Process, ProcessStep
from RCAIDE.Framework.Missions.Initialization import time,

# ----------------------------------------------------------------------------------------------------------------------
# Mission Segment
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class MissionInitialization(Process):

    name: str = 'Mission Initialization'

    time: ProcessStep = ProcessStep(name="Initialize Time")


@dataclass(kw_only=True)
class MissionIteration(Process):

    name: str = "Mission Iteration"

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
        self.append(self.initialization)
        self.append(self.iteration)
        self.append(self.finalization)



