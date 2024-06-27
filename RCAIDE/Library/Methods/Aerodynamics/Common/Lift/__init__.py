## @defgroup Library-Methods-Aerodynamics-Common-Lift Lift
# @ingroup Library-Methods-Aerodynamics-Common
# RCAIDE/Library/Methods/Aerodynamics/Common/Lift/__init__.py
# 

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 


from Legacy.trunk.S.Methods.Aerodynamics.Fidelity_Zero.Lift.compute_max_lift_coeff                         import compute_max_lift_coeff
from Legacy.trunk.S.Methods.Aerodynamics.Fidelity_Zero.Lift.compute_flap_lift                              import compute_flap_lift
from Legacy.trunk.S.Methods.Aerodynamics.Fidelity_Zero.Lift.compute_slat_lift                              import compute_slat_lift 
from .BET_sectional_properties                                                                             import compute_section_coefficients
from .BET_sectional_properties                                                                             import compute_inflow_and_tip_loss
from .fuselage_correction                                                                                  import fuselage_correction
from .total_lift                                                                                           import total_lift
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.generate_propeller_grid                 import generate_propeller_grid
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.generate_wing_wake_grid                 import generate_wing_wake_grid
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.compute_wing_wake                       import compute_wing_wake
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.compute_propeller_nonuniform_freestream import compute_propeller_nonuniform_freestream
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Helper_Functions.wave_drag_lift              import wave_drag_lift