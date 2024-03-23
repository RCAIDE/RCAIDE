## @defgroup Framework-Methods " + f"Performance
# RCAIDE/Library/Methods/Performance/__init__.py
#

"""RCAIDE Framework Package Setup.
"""
# ------------------------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------------------------
# @ingroup Methods

from .estimate_cruise_drag import _estimate_cruise_drag as estimate_cruise_drag
from .Legacy.trunk.S.Methods.Performance.estimate_take_off_field_length import _estimate_take_off_field_length as estimate_take_off_field_length
from .estimate_stall_speed import _estimate_stall_speed as estimate_stall_speed
from .Legacy.trunk.S.Methods.Performance.payload_range import _payload_range as payload_range
from .Legacy.trunk.S.Methods.Performance.estimate_landing_field_length import _estimate_landing_field_length as estimate_landing_field_length
from .Legacy.trunk.S.Methods.Performance.find_take_off_weight_given_tofl import _find_take_off_weight_given_tofl as find_take_off_weight_given_tofl
from .Legacy.trunk.S.Methods.Performance.V_n_diagram import _V_n_diagram as V_n_diagram
from .Legacy.trunk.S.Methods.Performance.propeller_range_endurance_speeds import _propeller_range_endurance_speeds as propeller_range_endurance_speeds
from .Legacy.trunk.S.Methods.Performance.propeller_range_endurance_speeds import _stall_speed as stall_speed
from .Legacy.trunk.S.Methods.Performance.electric_V_h_diagram import _electric_V_h_diagram as electric_V_h_diagram
from .Legacy.trunk.S.Methods.Performance.propeller_single_point import _propeller_single_point as propeller_single_point
from .Legacy.trunk.S.Methods.Performance.electric_payload_range import _electric_payload_range as electric_payload_range
from .Legacy.trunk.S.Methods.Performance.maximum_lift_to_drag import _maximum_lift_to_drag as maximum_lift_to_drag
