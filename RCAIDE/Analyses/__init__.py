## @defgroup Analyses
# RCAIDE/__init__.py
# (c) Copyright The Board of Trustees of RCAIDE

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from Legacy.trunk.S.Analyses.Analysis import Analysis

from Legacy.trunk.S.Analyses.Analysis  import Analysis
from Legacy.trunk.S.Analyses.Sizing    import Sizing
from Legacy.trunk.S.Analyses.Process   import Process
from Legacy.trunk.S.Analyses.Settings  import Settings
from Legacy.trunk.S.Analyses.Vehicle   import Vehicle

from . import Aerodynamics
from . import Stability
from . import Energy
from . import Weights
from . import Mission
from . import Atmospheric
from . import Planets
from . import Propulsion
from . import Sizing
from . import Noise
from . import Costs