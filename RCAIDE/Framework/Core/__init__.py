## @defgroup Core
# RCAIDE/Core/__init__.py
# 

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from Legacy.trunk.S.Core           import Data
from Legacy.trunk.S.Core           import DataOrdered
from Legacy.trunk.S.Core           import Diffed_Data, diff
from Legacy.trunk.S.Core           import ContainerOrdered
from Legacy.trunk.S.Core           import *
from .Container                    import Container
from .Utilities                    import interp2d
from .Utilities                    import orientation_product
from .Utilities                    import orientation_transpose
from .Utilities                    import angles_to_dcms
from Legacy.trunk.S.Core           import Units