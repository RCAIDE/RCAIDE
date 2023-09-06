## @defgroup Methods-Aerodynamics-AVL AVL 
# @ingroup Methods-Aerodynamics
# RCAIDE/Methods/Aerodynamics/AVL/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

from Legacy.trunk.S.Methods.Aerodynamics.AVL.create_avl_datastructure import translate_avl_wing, translate_avl_body , populate_wing_sections, populate_body_sections
from Legacy.trunk.S.Methods.Aerodynamics.AVL.purge_files              import purge_files
from Legacy.trunk.S.Methods.Aerodynamics.AVL.read_results             import read_results
from Legacy.trunk.S.Methods.Aerodynamics.AVL.run_analysis             import run_analysis
from Legacy.trunk.S.Methods.Aerodynamics.AVL.translate_data           import translate_conditions_to_cases, translate_results_to_conditions
from Legacy.trunk.S.Methods.Aerodynamics.AVL.write_geometry           import write_geometry
from Legacy.trunk.S.Methods.Aerodynamics.AVL.write_mass_file          import write_mass_file
from Legacy.trunk.S.Methods.Aerodynamics.AVL.write_input_deck         import write_input_deck
from Legacy.trunk.S.Methods.Aerodynamics.AVL.write_run_cases          import write_run_cases
from Legacy.trunk.S.Methods.Aerodynamics.AVL.write_avl_airfoil_file   import write_avl_airfoil_file

from . import Data
