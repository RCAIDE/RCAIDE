## @defgroup Analyses-Mission-Segments-Descent Descent
# RCAIDE/Analyses/Mission/Segments/Descent/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

"""RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .Constant_Speed_Constant_Angle       import Constant_Speed_Constant_Angle
from .Constant_Speed_Constant_Angle_Noise import Constant_Speed_Constant_Angle_Noise
from .Constant_Speed_Constant_Rate        import Constant_Speed_Constant_Rate
from .Linear_Mach_Constant_Rate           import Linear_Mach_Constant_Rate
from .Constant_EAS_Constant_Rate          import Constant_EAS_Constant_Rate
from .Constant_CAS_Constant_Rate          import Constant_CAS_Constant_Rate
from .Unknown_Throttle                    import Unknown_Throttle