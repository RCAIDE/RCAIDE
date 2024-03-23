## @defgroup Framework-Methods-Aerodynamics " + f"Vortex_Lattice_Method
# RCAIDE/Library/Methods/Aerodynamics/Vortex_Lattice_Method/__init__.py
#

"""RCAIDE Framework Package Setup.
"""
# ------------------------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------------------------
# @ingroup Methods-Aerodynamics

from .Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift import _generate_vortex_distribution as generate_vortex_distribution
from .Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift import _compute_unit_normal as compute_unit_normal
from .Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.generate_VD_helpers import _postprocess_VD as postprocess_VD
from .Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.generate_VD_helpers import _compute_panel_area as compute_panel_area
from .Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.generate_VD_helpers import _compute_unit_normal as compute_unit_normal
from .Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.make_VLM_wings import _make_VLM_wings as make_VLM_wings
from .Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.deflect_control_surface import _deflect_control_surface as deflect_control_surface
from .compute_RHS_matrix import _compute_RHS_matrix as compute_RHS_matrix
from .compute_wing_induced_velocity import _compute_wing_induced_velocity as compute_wing_induced_velocity
from .generate_vortex_distribution import _generate_vortex_distribution as generate_vortex_distribution
from .VLM import _VLM as VLM
