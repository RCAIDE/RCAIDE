## @defgroup Methods-Utilities Utilities
# RCAIDE/Methods/Utilities/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# @ingroup Methods

from . import Chebyshev

from Legacy.trunk.S.Methods.Utilities.soft_max                 import soft_max
from Legacy.trunk.S.Methods.Utilities.latin_hypercube_sampling import latin_hypercube_sampling
from Legacy.trunk.S.Methods.Utilities.Cubic_Spline_Blender     import Cubic_Spline_Blender