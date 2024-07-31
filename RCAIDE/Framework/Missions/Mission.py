# RCAIDE/Framework/Missions/Mission.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field
from warnings import warn

# RCAIDE Imports

from RCAIDE.Framework.Core import Process, ProcessStep

# ----------------------------------------------------------------------------------------------------------------------
# Mission Segment
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class MissionSegment(ProcessStep):

    analyses: list[Process] = field(default_factory=list)