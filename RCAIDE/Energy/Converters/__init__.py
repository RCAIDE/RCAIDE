## @defgroup Energy-Converters Converters
# RCAIDE/Energy/Converters/__init__.py
# 

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

## @ingroup Energy

from Legacy.trunk.S.Components.Energy.Converters import Combustor
from Legacy.trunk.S.Components.Energy.Converters import Compressor
from Legacy.trunk.S.Components.Energy.Converters import Compression_Nozzle
from Legacy.trunk.S.Components.Energy.Converters import de_Laval_Nozzle
from Legacy.trunk.S.Components.Energy.Converters import Expansion_Nozzle
from .Fan                                        import Fan
from .Ducted_Fan                                 import Ducted_Fan
from Legacy.trunk.S.Components.Energy.Converters import Fuel_Cell
from Legacy.trunk.S.Components.Energy.Converters import Gearbox
from Legacy.trunk.S.Components.Energy.Converters import Generator_Zero_Fid
from .Engine                                     import Engine
from .Lift_Rotor                                 import Lift_Rotor
from Legacy.trunk.S.Components.Energy.Converters import Motor_HTS_Rotor
from Legacy.trunk.S.Components.Energy.Converters import Motor_Lo_Fid
from .Motor                                      import Motor
from Legacy.trunk.S.Components.Energy.Converters import Propeller_Lo_Fid
from .Propeller                                  import Propeller
from Legacy.trunk.S.Components.Energy.Converters import Ram
from Legacy.trunk.S.Components.Energy.Converters import Rocket_Combustor
from .Rotor                                      import Rotor
from .Prop_Rotor                                 import Prop_Rotor
from Legacy.trunk.S.Components.Energy.Converters import Shaft_Power_Off_Take
from Legacy.trunk.S.Components.Energy.Converters import Solar_Panel
from Legacy.trunk.S.Components.Energy.Converters import Supersonic_Nozzle
from Legacy.trunk.S.Components.Energy.Converters import Turbine
from .Turbofan                                   import Turbofan
from .Turbojet                                   import Turbojet
from Legacy.trunk.S.Components.Energy.Converters import Turboelectric

