## @defgroup Analyses
# RCAIDE/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .Analysis  import Analysis 
from .Process   import Process
from .Settings  import Settings
from .Vehicle   import Vehicle

from . import Aerodynamics
from . import Stability
from . import Energy
from . import Weights
from . import Mission
from . import Atmospheric
from . import Planets
from . import Propulsion 
from . import Noise
from . import Costs