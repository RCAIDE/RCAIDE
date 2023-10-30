## @defgroup Analyses-Aerodynamics Aerodynamics
# RCAIDE/Analyses/Aerodynamics/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

"""RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from Legacy.trunk.S.Analyses.Aerodynamics.Aerodynamics                 import Aerodynamics
from Legacy.trunk.S.Analyses.Aerodynamics.AVL                          import AVL
from Legacy.trunk.S.Analyses.Aerodynamics.AVL_Inviscid                 import AVL_Inviscid
from Legacy.trunk.S.Analyses.Aerodynamics.Fidelity_Zero                import Fidelity_Zero
from Legacy.trunk.S.Analyses.Aerodynamics.Markup                       import Markup
from Legacy.trunk.S.Analyses.Aerodynamics.Process_Geometry             import Process_Geometry
from Legacy.trunk.S.Analyses.Aerodynamics.Supersonic_Zero              import Supersonic_Zero
from Legacy.trunk.S.Analyses.Aerodynamics.Vortex_Lattice               import Vortex_Lattice
from Legacy.trunk.S.Analyses.Aerodynamics.AERODAS                      import AERODAS
from Legacy.trunk.S.Analyses.Aerodynamics.SU2_Euler                    import SU2_Euler
from Legacy.trunk.S.Analyses.Aerodynamics.SU2_inviscid                 import SU2_inviscid
from Legacy.trunk.S.Analyses.Aerodynamics.SU2_Euler_Super              import SU2_Euler_Super
from Legacy.trunk.S.Analyses.Aerodynamics.SU2_inviscid_Super           import SU2_inviscid_Super
from Legacy.trunk.S.Analyses.Aerodynamics.Supersonic_OpenVSP_Wave_Drag import Supersonic_OpenVSP_Wave_Drag
from Legacy.trunk.S.Analyses.Aerodynamics.Lifting_Line                 import Lifting_Line
from . import Airfoils