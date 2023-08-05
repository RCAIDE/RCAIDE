## @defgroup Methods-Missions-Segments Segments
# RCAIDE/Methods/Mission/Segments/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# @ingroup Methods-Mission

from . import Common
from . import Cruise
from . import Climb
from . import Descent
from . import Ground
from . import Hover
from . import Single_Point
from . import Transition

from Legacy.trunk.S.Methods.Missions.Segments  import converge_root
from Legacy.trunk.S.Methods.Missions.Segments  import expand_state
from Legacy.trunk.S.Methods.Missions.Segments  import converge_opt
