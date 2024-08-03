# RCAIDE/Framework/Missions/Mission.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field

# RCAIDE Imports

from RCAIDE.Reference.Core import Process, ProcessStep

# ----------------------------------------------------------------------------------------------------------------------
# Mission Segment
# ----------------------------------------------------------------------------------------------------------------------

@dataclass(kw_only=True)
class Iterate(Process):

    name: str = "Iterate"

    def __post_init__(self):

        initialization = Process(name="Iterate Initials")
        time = ProcessStep(name="Initialize Time")




@dataclass(kw_only=True)
class MissionSegment(Process):

    name: str = "Mission Segment"

    Settings: dataclass = dataclass(kw_only=True)

    analyses: list[Process] = field(default_factory=list)

    def __post_init__(self):
        return None



