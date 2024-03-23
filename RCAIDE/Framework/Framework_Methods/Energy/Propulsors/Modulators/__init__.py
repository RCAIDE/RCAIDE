## @defgroup Framework-Methods-Energy-Propulsors " + f"Modulators
# RCAIDE/Library/Methods/Energy/Propulsors/Modulators/__init__.py
#

"""RCAIDE Framework Package Setup.
"""
# ------------------------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------------------------
# @ingroup Methods-Energy-Propulsors

from .compute_esc_performance import _compute_voltage_out_from_throttle as compute_voltage_out_from_throttle
from .compute_esc_performance import _compute_voltage_in_from_throttle as compute_voltage_in_from_throttle
from .compute_esc_performance import _compute_throttle_from_voltages as compute_throttle_from_voltages
from .compute_esc_performance import _compute_current_in_from_throttle as compute_current_in_from_throttle
