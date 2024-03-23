## @defgroup Framework-Methods-Energy-Sources-Battery " + f"Common
# RCAIDE/Library/Methods/Energy/Sources/Battery/Common/__init__.py
#

"""RCAIDE Framework Package Setup.
"""
# ------------------------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------------------------
# @ingroup Methods-Energy-Sources-Battery

from .append_initial_battery_conditions import _append_initial_battery_conditions as append_initial_battery_conditions
from .compute_net_generated_battery_heat import _compute_net_generated_battery_heat as compute_net_generated_battery_heat
from .find_ragone_properties import _find_ragone_properties as find_ragone_properties
from .find_specific_power import _find_specific_power as find_specific_power
from .find_ragone_optimum import _find_ragone_optimum as find_ragone_optimum
from .find_mass_gain_rate import _find_mass_gain_rate as find_mass_gain_rate
from .find_total_mass_gain import _find_total_mass_gain as find_total_mass_gain
from .initialize_from_mass import _initialize_from_mass as initialize_from_mass
from .initialize_from_energy_and_power import _initialize_from_energy_and_power as initialize_from_energy_and_power
from .initialize_from_circuit_configuration import _initialize_from_circuit_configuration as initialize_from_circuit_configuration
from .pack_battery_conditions import _pack_battery_conditions as pack_battery_conditions
