## @defgroup Methods-Performance Performance
# RCAIDE/Methods/Performance/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

"""RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .estimate_cruise_drag                                                import estimate_cruise_drag
from Legacy.trunk.S.Methods.Performance.estimate_take_off_field_length    import estimate_take_off_field_length
from Legacy.trunk.S.Methods.Performance.estimate_stall_speed              import estimate_stall_speed
from Legacy.trunk.S.Methods.Performance.payload_range                     import payload_range
from Legacy.trunk.S.Methods.Performance.estimate_landing_field_length     import estimate_landing_field_length
from Legacy.trunk.S.Methods.Performance.find_take_off_weight_given_tofl   import find_take_off_weight_given_tofl
from Legacy.trunk.S.Methods.Performance.V_n_diagram                       import V_n_diagram
from Legacy.trunk.S.Methods.Performance.propeller_range_endurance_speeds  import propeller_range_endurance_speeds, stall_speed
from Legacy.trunk.S.Methods.Performance.electric_V_h_diagram              import electric_V_h_diagram
from Legacy.trunk.S.Methods.Performance.propeller_single_point            import propeller_single_point
from Legacy.trunk.S.Methods.Performance.electric_payload_range            import electric_payload_range
from Legacy.trunk.S.Methods.Performance.maximum_lift_to_drag              import maximum_lift_to_drag
