## @defgroup Framework-Methods-Energy-Propulsors-Converters " + f"Rotor
# RCAIDE/Library/Methods/Energy/Propulsors/Converters/Rotor/__init__.py
#

"""RCAIDE Framework Package Setup.
"""
# ------------------------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------------------------
# @ingroup Methods-Energy-Propulsors-Converters

from . import _Design as Design
from . import _Wake as Wake
from .design_propeller import _design_propeller as design_propeller
from .design_lift_rotor import _design_lift_rotor as design_lift_rotor
from .design_prop_rotor import _design_prop_rotor as design_prop_rotor
