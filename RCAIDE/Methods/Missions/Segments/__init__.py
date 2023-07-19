## @defgroup Methods-Missions-Segments Segments
# RCAIDE/Methods/Mission/Segments/__init__.py
# (c) Copyright The Board of Trustees of RCAIDE

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# @ingroup Methods-Mission

from .converge_root import converge_root
from .expand_state  import expand_state
from .optimize      import converge_opt

from . import Common
from . import Cruise
from . import Climb
from . import Descent
from . import Ground
from . import Hover
from . import Single_Point
from . import Transition
