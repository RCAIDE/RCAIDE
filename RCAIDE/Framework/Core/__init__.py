## @defgroup Core
# RCAIDE/Core/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from Legacy.trunk.S.Core           import Data
from Legacy.trunk.S.Core           import DataOrdered
from Legacy.trunk.S.Core           import Diffed_Data, diff
from .Container                    import Container 
from Legacy.trunk.S.Core           import *
from Legacy.trunk.S.Core           import Units
from .Utilities                    import interp2d
from .Utilities                    import orientation_product
from .Utilities                    import orientation_transpose
from .Utilities                    import angles_to_dcms
from .Utilities                    import args_passer
from .Process                      import Process, ProcessStep