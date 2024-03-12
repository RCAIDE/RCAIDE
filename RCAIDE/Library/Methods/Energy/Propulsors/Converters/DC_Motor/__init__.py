## @defgroup Methods-Components-Propulsors-Converters-DC_Motor 
# RCAIDE/Methods/Energy/Propulsors/Converters/DC_Motor/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .motor_performance                 import compute_I_from_omega_and_V
from .motor_performance                 import compute_omega_and_Q_from_Cp_and_V
from .motor_performance                 import compute_Q_from_omega_and_V
from .motor_performance                 import compute_V_and_I_from_omega_and_Kv
from .size_motor_from_Kv                import size_motor_from_Kv
from .size_motor_from_mass              import size_motor_from_mass
from .design_motor                      import design_motor