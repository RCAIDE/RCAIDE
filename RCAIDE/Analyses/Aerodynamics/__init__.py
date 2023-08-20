## @defgroup Analyses-Aerodynamics Aerodynamics
# RCAIDE/Analyses/Aerodynamics/__init__.py
# (c) Copyright The Board of Trustees of RCAIDE

"""RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .Aerodynamics                                                     import Aerodynamics
from Legacy.trunk.S.Analyses.Aerodynamics.AVL                          import AVL
from Legacy.trunk.S.Analyses.Aerodynamics.AVL_Inviscid                 import AVL_Inviscid
from .Fidelity_Zero                                                    import Fidelity_Zero
from .Markup                                                           import Markup
from .Process_Geometry                                                 import Process_Geometry
from Legacy.trunk.S.Analyses.Aerodynamics.Supersonic_Zero              import Supersonic_Zero
from .Vortex_Lattice                                                   import Vortex_Lattice
from Legacy.trunk.S.Analyses.Aerodynamics.AERODAS                      import AERODAS
from Legacy.trunk.S.Analyses.Aerodynamics.SU2_Euler                    import SU2_Euler
from Legacy.trunk.S.Analyses.Aerodynamics.SU2_inviscid                 import SU2_inviscid
from Legacy.trunk.S.Analyses.Aerodynamics.SU2_Euler_Super              import SU2_Euler_Super
from Legacy.trunk.S.Analyses.Aerodynamics.SU2_inviscid_Super           import SU2_inviscid_Super
from Legacy.trunk.S.Analyses.Aerodynamics.Supersonic_OpenVSP_Wave_Drag import Supersonic_OpenVSP_Wave_Drag
from Legacy.trunk.S.Analyses.Aerodynamics.Lifting_Line                 import Lifting_Line