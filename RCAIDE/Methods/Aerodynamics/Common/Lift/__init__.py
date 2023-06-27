## @defgroup Methods-Aerodynamics-Common-Fidelity_Zero-Lift Lift
# Lift methods that are directly specified by analyses.
# @ingroup Methods-Aerodynamics-Common-Fidelity_Zero

from Legacy.trunk.S.Methods.Common.Lift.aircraft_total                          import aircraft_total
from Legacy.trunk.S.Methods.Common.Lift.compute_RHS_matrix                      import compute_RHS_matrix 
from Legacy.trunk.S.Methods.Common.Lift.compute_wing_induced_velocity           import compute_wing_induced_velocity 
from Legacy.trunk.S.Methods.Common.Lift.generate_propeller_grid                 import generate_propeller_grid
from Legacy.trunk.S.Methods.Common.Lift.generate_wing_wake_grid                 import generate_wing_wake_grid
from Legacy.trunk.S.Methods.Common.Lift.compute_wing_wake                       import compute_wing_wake
from Legacy.trunk.S.Methods.Common.Lift.compute_propeller_nonuniform_freestream import compute_propeller_nonuniform_freestream
from Legacy.trunk.S.Methods.Common.Lift.generate_vortex_distribution            import generate_vortex_distribution, compute_unit_normal 
from Legacy.trunk.S.Methods.Common.Lift.fuselage_correction                     import fuselage_correction
from Legacy.trunk.S.Methods.Common.Lift.make_VLM_wings                          import make_VLM_wings
from Legacy.trunk.S.Methods.Common.Lift.VLM                                     import VLM