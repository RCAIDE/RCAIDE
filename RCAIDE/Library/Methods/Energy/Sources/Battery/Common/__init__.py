## @defgroup Library-Methods-Energy-Sources-Battery-Common Common
# RCAIDE/Library/Methods/Energy/Sources/Battery/Common/__init__.py 
# (c) Copyright 2023 Aerospace Research Community LLC

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# @ingroup Methods-Energy-Sources-Battery

from .append_initial_battery_conditions     import append_initial_battery_conditions 
from .compute_net_generated_battery_heat    import compute_net_generated_battery_heat
from .compute_ragone_properties             import compute_ragone_properties
from .compute_specific_power                import compute_specific_power
from .compute_ragone_optimum                import compute_ragone_optimum
from .compute_mass_gain_rate                import compute_mass_gain_rate
from .compute_total_mass_gain               import compute_total_mass_gain
from .size_pack_from_mass                   import initialize_from_mass
from .size_pack_from_energy_and_power       import initialize_from_energy_and_power
from .size_pack_from_circuit_configuration  import initialize_from_circuit_configuration
from .pack_battery_conditions               import pack_battery_conditions 