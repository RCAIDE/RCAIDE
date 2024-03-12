## @defgroup Components-Propulsors-Converters Converters
# RCAIDE/Components/Propulsors/Converters/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

## @ingroup Energy

from .Combustor                                  import Combustor
from .Compressor                                 import Compressor
from .Compression_Nozzle                         import Compression_Nozzle
from Legacy.trunk.S.Components.Energy.Converters import de_Laval_Nozzle
from .Expansion_Nozzle                           import Expansion_Nozzle
from .Fan                                        import Fan
from Legacy.trunk.S.Components.Energy.Converters import Fuel_Cell
from Legacy.trunk.S.Components.Energy.Converters import Gearbox
from Legacy.trunk.S.Components.Energy.Converters import Generator_Zero_Fid
from .Engine                                     import Engine
from .Lift_Rotor                                 import Lift_Rotor
from Legacy.trunk.S.Components.Energy.Converters import Motor_HTS_Rotor
from Legacy.trunk.S.Components.Energy.Converters import Motor_Lo_Fid
from .DC_Motor                                   import DC_Motor
from Legacy.trunk.S.Components.Energy.Converters import Propeller_Lo_Fid
from .Propeller                                  import Propeller
from .Ram                                        import Ram
from Legacy.trunk.S.Components.Energy.Converters import Rocket_Combustor
from .Rotor                                      import Rotor
from .Prop_Rotor                                 import Prop_Rotor
from .Shaft_Power_Offtake                        import Shaft_Power_Offtake
from Legacy.trunk.S.Components.Energy.Converters import Solar_Panel
from Legacy.trunk.S.Components.Energy.Converters import Supersonic_Nozzle
from .Turbine                                    import Turbine

