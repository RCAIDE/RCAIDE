## @defgroup Framework-Methods-Aerodynamics-Common " + f"Lift
# RCAIDE/Library/Methods/Aerodynamics/Common/Lift/__init__.py
#

"""RCAIDE Framework Package Setup.
"""
# ------------------------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------------------------
# @ingroup Methods-Aerodynamics-Common

from .Legacy.trunk.S.Methods.Aerodynamics.Fidelity_Zero.Lift.compute_max_lift_coeff import _compute_max_lift_coeff as compute_max_lift_coeff
from .Legacy.trunk.S.Methods.Aerodynamics.Fidelity_Zero.Lift.compute_flap_lift import _compute_flap_lift as compute_flap_lift
from .Legacy.trunk.S.Methods.Aerodynamics.Fidelity_Zero.Lift.compute_slat_lift import _compute_slat_lift as compute_slat_lift
from .BET_calculations import _compute_airfoil_aerodynamics as compute_airfoil_aerodynamics
from .BET_calculations import _compute_inflow_and_tip_loss as compute_inflow_and_tip_loss
from .fuselage_correction import _fuselage_correction as fuselage_correction
from .aircraft_total import _aircraft_total as aircraft_total
from .Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.generate_propeller_grid import _generate_propeller_grid as generate_propeller_grid
from .Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.generate_wing_wake_grid import _generate_wing_wake_grid as generate_wing_wake_grid
from .Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.compute_wing_wake import _compute_wing_wake as compute_wing_wake
from .Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.compute_propeller_nonuniform_freestream import _compute_propeller_nonuniform_freestream as compute_propeller_nonuniform_freestream
