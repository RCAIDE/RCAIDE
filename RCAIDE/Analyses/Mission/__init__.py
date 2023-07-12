## @defgroup Analyses-Mission Mission
# RCAIDE/Analyses/Mission/__init__.py
# (c) Copyright The Board of Trustees of RCAIDE

"""RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from Legacy.trunk.S.Analyses.Mission.All_At_Once import All_At_Once
from .Mission import Mission
from .Sequential_Segments import Sequential_Segments

# packages
from . import Segments
from . import Variable_Range_Cruise