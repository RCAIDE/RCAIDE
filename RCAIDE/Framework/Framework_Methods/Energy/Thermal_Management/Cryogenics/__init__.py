## @defgroup Framework-Methods-Energy-Thermal_Management " + f"Cryogenics
# RCAIDE/Library/Methods/Energy/Thermal_Management/Cryogenics/__init__.py
#

"""RCAIDE Framework Package Setup.
"""
# ------------------------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------------------------
# @ingroup Methods-Energy-Thermal_Management

from .cryocooler_model import _cryocooler_model as cryocooler_model
from .dynamo_efficiency import _efficiency_curve as efficiency_curve
from .compute_minimum_power import _compute_minimum_power as compute_minimum_power
from .compute_cryogen_mass_flow_rate import _compute_cryogen_mass_flow_rate as compute_cryogen_mass_flow_rate
