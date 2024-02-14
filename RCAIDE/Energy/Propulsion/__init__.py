## @defgroup Energy-Propulsion Propulsion
# RCAIDE/Energy/Propulsion/__init__.py
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
from Legacy.trunk.S.Components.Energy.Converters import Turboelectric
