## @defgroup Methods-Energy-Propulsors-Converters-Motor 
# RCAIDE/Methods/Energy/Propulsors/Converters/Motor/__init__.py
# 

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .compute_I_from_omega_and_V        import compute_I_from_omega_and_V
from .compute_omega_and_Q_from_Cp_and_V import compute_omega_and_Q_from_Cp_and_V
from .compute_Q_from_omega_and_V        import compute_Q_from_omega_and_V
from .compute_V_and_I_from_omega_and_Kv import compute_V_and_I_from_omega_and_Kv
from .size_motor_from_Kv                import size_motor_from_Kv
from .size_motor_from_mass              import size_motor_from_mass
from .design_motor                      import design_motor