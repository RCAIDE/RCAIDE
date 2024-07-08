# RCAIDE/Library/Methods/Energy/Propulsors/Converters/DC_Motor/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .motor_performance                 import compute_torque_from_RPM_and_voltage
from .motor_performance                 import compute_RPM_and_torque_from_power_coefficent_and_voltage
from .motor_performance                 import compute_current_from_RPM_and_voltage
from .motor_performance                 import compute_voltage_and_current_from_RPM_and_speed_constant
from .size_motor_from_KV                import size_motor_from_KV
from .size_motor_from_mass              import size_motor_from_mass
from .design_motor                      import design_motor