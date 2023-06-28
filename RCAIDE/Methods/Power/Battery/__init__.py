## @defgroup Methods-Power-Battery Battery
# RCAIDE/Methods/Power/Battery/__init__.py
# (c) Copyright The Board of Trustees of RCAIDE

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# @ingroup Methods-Power

from . import Ragone
from . import Sizing
from . import Variable_Mass
from . import Cell_Cycle_Models

from Legacy.trunk.S.Methods.Power.Battery    import append_initial_battery_conditions
from Legacy.trunk.S.Methods.Power.Battery    import compute_net_generated_battery_heat
from Legacy.trunk.S.Methods.Power.Battery    import pack_battery_conditions