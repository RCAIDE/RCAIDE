## @defgroup Energy-Propulsors Propulsors
# RCAIDE/Energy/Propulsors/__init__.py
# 

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .          import Converters 
from .          import Modulators 
from .Propulsor import Propulsor

from .Electric_Rotor                             import Electric_Rotor
from .ICE_Propeller                              import ICE_Propeller
from .Turbofan                                   import Turbofan
from .Turbojet                                   import Turbojet
from .Constant_Speed_ICE_Propeller               import Constant_Speed_ICE_Propeller
