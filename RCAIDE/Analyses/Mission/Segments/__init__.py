## @defgroup Analyses-Mission-Segments Segments
# RCAIDE/Analyses/Mission/Segments/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

"""RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .Segment     import Segment
from .Simple      import Simple
from .Aerodynamic import Aerodynamic

from . import Climb
from . import Conditions
from . import Cruise
from . import Descent
from . import Ground
from . import Hover
from . import Single_Point
from . import Transition