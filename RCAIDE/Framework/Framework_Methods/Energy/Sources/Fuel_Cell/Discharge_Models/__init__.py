## @defgroup Framework-Methods-Energy-Sources-Fuel_Cell " + f"Discharge_Models
# RCAIDE/Library/Methods/Energy/Sources/Fuel_Cell/Discharge_Models/__init__.py
#

"""RCAIDE Framework Package Setup.
"""
# ------------------------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------------------------
# @ingroup Methods-Energy-Sources-Fuel_Cell

from .Legacy.trunk.S.Methods.Power.Fuel_Cell.Discharge.zero_fidelity import _zero_fidelity as zero_fidelity
from .Legacy.trunk.S.Methods.Power.Fuel_Cell.Discharge.larminie import _larminie as larminie
from .Legacy.trunk.S.Methods.Power.Fuel_Cell.Discharge.setup_larminie import _setup_larminie as setup_larminie
from .Legacy.trunk.S.Methods.Power.Fuel_Cell.Discharge.find_voltage_larminie import _find_voltage_larminie as find_voltage_larminie
from .Legacy.trunk.S.Methods.Power.Fuel_Cell.Discharge.find_power_larminie import _find_power_larminie as find_power_larminie
from .Legacy.trunk.S.Methods.Power.Fuel_Cell.Discharge.find_power_diff_larminie import _find_power_diff_larminie as find_power_diff_larminie
