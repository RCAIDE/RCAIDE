## @defgroup Framework-Methods-Energy-Propulsors-Converters " + f"DC_Motor
# RCAIDE/Library/Methods/Energy/Propulsors/Converters/DC_Motor/__init__.py
#

"""RCAIDE Framework Package Setup.
"""
# ------------------------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------------------------
# @ingroup Methods-Energy-Propulsors-Converters

from .motor_performance import _compute_I_from_omega_and_V as compute_I_from_omega_and_V
from .motor_performance import _compute_omega_and_Q_from_Cp_and_V as compute_omega_and_Q_from_Cp_and_V
from .motor_performance import _compute_Q_from_omega_and_V as compute_Q_from_omega_and_V
from .motor_performance import _compute_V_and_I_from_omega_and_Kv as compute_V_and_I_from_omega_and_Kv
from .size_motor_from_Kv import _size_motor_from_Kv as size_motor_from_Kv
from .size_motor_from_mass import _size_motor_from_mass as size_motor_from_mass
from .design_motor import _design_motor as design_motor
