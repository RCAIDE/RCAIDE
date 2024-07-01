## @defgroup Methods-Geometry-Two_Dimensional/Planform Planform
# RCAIDE/Methods/Geometry/Two_Dimensional/Planform/__init__.py
# 

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# @ingroup Methods-Geometry-Two_Dimensional
from .wing_segmented_planform                                 import wing_segmented_planform, segment_properties

from Legacy.trunk.S.Methods.Geometry.Two_Dimensional.Planform import populate_control_sections as populate_control_sections  
from Legacy.trunk.S.Methods.Flight_Dynamics.Static_Stability.Approximations.Supporting_Functions import  convert_sweep as  convert_sweep
from Legacy.trunk.S.Methods.Geometry.Two_Dimensional.Planform import fuselage_planform
from Legacy.trunk.S.Methods.Geometry.Two_Dimensional.Planform import horizontal_tail_planform
from Legacy.trunk.S.Methods.Geometry.Two_Dimensional.Planform import vertical_tail_planform
from Legacy.trunk.S.Methods.Geometry.Two_Dimensional.Planform import wing_planform
from Legacy.trunk.S.Methods.Geometry.Two_Dimensional.Planform import horizontal_tail_planform_raymer
from Legacy.trunk.S.Methods.Geometry.Two_Dimensional.Planform import set_origin_non_dimensional, set_origin_dimensional
from Legacy.trunk.S.Methods.Geometry.Two_Dimensional.Planform import vertical_tail_planform_raymer
from Legacy.trunk.S.Methods.Geometry.Two_Dimensional.Planform import wing_fuel_volume
from Legacy.trunk.S.Methods.Geometry.Three_Dimensional.compute_span_location_from_chord_length    import compute_span_location_from_chord_length
from Legacy.trunk.S.Methods.Geometry.Three_Dimensional.compute_chord_length_from_span_location    import compute_chord_length_from_span_location 
