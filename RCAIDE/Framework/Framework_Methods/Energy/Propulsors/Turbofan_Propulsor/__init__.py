## @defgroup Framework-Methods-Energy-Propulsors " + f"Turbofan_Propulsor
# RCAIDE/Library/Methods/Energy/Propulsors/Turbofan_Propulsor/__init__.py
#

"""RCAIDE Framework Package Setup.
"""
# ------------------------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------------------------
# @ingroup Methods-Energy-Propulsors

from .compute_stream_thrust import _compute_stream_thrust as compute_stream_thrust
from .compute_thurst import _compute_thrust as compute_thrust
from .size_core import _size_core as size_core
from .size_stream_thrust import _size_stream_thrust as size_stream_thrust
from .compute_turbofan_performance import _compute_turbofan_performance as compute_turbofan_performance
from .design_turbofan import _design_turbofan as design_turbofan
from .compute_nacelle_geometry import _compute_nacelle_geometry as compute_nacelle_geometry
from .Legacy.trunk.S.Methods.Propulsion.turbofan_emission_index import _turbofan_emission_index as turbofan_emission_index
