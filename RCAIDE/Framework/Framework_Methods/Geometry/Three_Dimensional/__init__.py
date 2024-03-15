## @defgroup Framework-Methods-Geometry " + f"Three_Dimensional
# RCAIDE/Library/Methods/Geometry/Three_Dimensional/__init__.py
#

"""RCAIDE Framework Package Setup.
"""
# ------------------------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------------------------
# @ingroup Methods-Geometry

from .convert_wing_sweep import _convert_wing_sweep as convert_wing_sweep
from .convert_segmented_wing_sweep import _convert_segmented_wing_sweep as convert_segmented_wing_sweep
from .Legacy.trunk.S.Methods.Geometry.Three_Dimensional.estimate_naca_4_series_internal_volume import _estimate_naca_4_series_internal_volume as estimate_naca_4_series_internal_volume
from .Legacy.trunk.S.Methods.Geometry.Three_Dimensional.compute_span_location_from_chord_length import _compute_span_location_from_chord_length as compute_span_location_from_chord_length
from .Legacy.trunk.S.Methods.Geometry.Three_Dimensional.compute_chord_length_from_span_location import _compute_chord_length_from_span_location as compute_chord_length_from_span_location
