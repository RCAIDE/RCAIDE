## @defgroup Analyses-Mission-Segments-Ground Ground
# RCAIDE/Analyses/Mission/Segments/Ground/__init__.py
# (c) Copyright The Board of Trustees of RCAIDE

"""RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from Legacy.trunk.S.Analyses.Mission.Segments.Ground.Ground                   import Ground
from Legacy.trunk.S.Analyses.Mission.Segments.Ground.Landing                  import Landing
from Legacy.trunk.S.Analyses.Mission.Segments.Ground.Takeoff                  import Takeoff
from .Battery_Discharge import Battery_Discharge
from .Battery_Charge    import Battery_Charge