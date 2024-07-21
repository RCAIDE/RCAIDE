# RCAIDE/Methods/Aerodynamics/Fidelity_Zero/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift                                 import generate_vortex_distribution, compute_unit_normal 
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.generate_VD_helpers             import postprocess_VD, compute_panel_area, compute_unit_normal
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.make_VLM_wings                  import make_VLM_wings  
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.deflect_control_surface         import deflect_control_surface

from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.VLM                             import VLM 
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.compute_RHS_matrix              import compute_RHS_matrix 
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.compute_wing_induced_velocity   import compute_wing_induced_velocity 
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Lift.generate_vortex_distribution    import generate_vortex_distribution
 
from .train_VLM_surrogates                    import train_VLM_surrogates
from .build_VLM_surrogates                    import build_VLM_surrogates  
from .evaluate_VLM import *  

