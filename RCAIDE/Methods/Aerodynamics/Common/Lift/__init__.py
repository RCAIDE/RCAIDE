## @defgroup Methods-Aerodynamics-Common-Lift Lift
# @ingroup Methods-Aerodynamics-Common
# RCAIDE/Methods/Aerodynamics/Common/Lift/__init__.py
# (c) Copyright The Board of Trustees of RCAIDE

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.aircraft_total                          import aircraft_total
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.compute_RHS_matrix                      import compute_RHS_matrix 
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.compute_wing_induced_velocity           import compute_wing_induced_velocity 
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.generate_propeller_grid                 import generate_propeller_grid
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.generate_wing_wake_grid                 import generate_wing_wake_grid
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.compute_wing_wake                       import compute_wing_wake
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.compute_propeller_nonuniform_freestream import compute_propeller_nonuniform_freestream
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift                                         import generate_vortex_distribution, compute_unit_normal 
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.fuselage_correction                     import fuselage_correction
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.make_VLM_wings                          import make_VLM_wings
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.VLM                                     import VLM
from .BET_calculations                                                                                     import compute_airfoil_aerodynamics 
from .BET_calculations                                                                                     import compute_inflow_and_tip_loss