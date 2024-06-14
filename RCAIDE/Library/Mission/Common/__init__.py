## @defgroup Methods-Missions-Common Common
# RCAIDE/Methods/Mission/Common/__init__.py
# 

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# @ingroup Methods-Mission-Segments

from .   import Initialize
from .   import Pre_Process
from .   import Residuals
from .   import Unpack_Unknowns
from .   import Update

from .Segments import * 
from .compute_point_to_point_geospacial_data import compute_point_to_point_geospacial_data
 