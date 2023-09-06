## @defgroup Analyses-Mission Mission
# RCAIDE/Analyses/Mission/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

"""RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from Legacy.trunk.S.Analyses.Mission.All_At_Once import All_At_Once
from Legacy.trunk.S.Analyses.Mission.Mission import Mission
from Legacy.trunk.S.Analyses.Mission.Sequential_Segments import Sequential_Segments

# packages
from . import Segments
from . import Variable_Range_Cruise