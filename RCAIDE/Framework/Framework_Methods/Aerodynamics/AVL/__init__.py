## @defgroup Framework-Methods-Aerodynamics " + f"AVL
# RCAIDE/Library/Methods/Aerodynamics/AVL/__init__.py
#

"""RCAIDE Framework Package Setup.
"""
# ------------------------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------------------------
# @ingroup Methods-Aerodynamics

from .Legacy.trunk.S.Methods.Aerodynamics.AVL.create_avl_datastructure import _translate_avl_wing as translate_avl_wing
from .Legacy.trunk.S.Methods.Aerodynamics.AVL.create_avl_datastructure import _translate_avl_body as translate_avl_body
from .Legacy.trunk.S.Methods.Aerodynamics.AVL.create_avl_datastructure import _populate_wing_sections as populate_wing_sections
from .Legacy.trunk.S.Methods.Aerodynamics.AVL.create_avl_datastructure import _populate_body_sections as populate_body_sections
from .Legacy.trunk.S.Methods.Aerodynamics.AVL.purge_files import _purge_files as purge_files
from .Legacy.trunk.S.Methods.Aerodynamics.AVL.read_results import _read_results as read_results
from .Legacy.trunk.S.Methods.Aerodynamics.AVL.run_analysis import _run_analysis as run_analysis
from .Legacy.trunk.S.Methods.Aerodynamics.AVL.translate_data import _translate_conditions_to_cases as translate_conditions_to_cases
from .Legacy.trunk.S.Methods.Aerodynamics.AVL.translate_data import _translate_results_to_conditions as translate_results_to_conditions
from .Legacy.trunk.S.Methods.Aerodynamics.AVL.write_geometry import _write_geometry as write_geometry
from .Legacy.trunk.S.Methods.Aerodynamics.AVL.write_mass_file import _write_mass_file as write_mass_file
from .Legacy.trunk.S.Methods.Aerodynamics.AVL.write_input_deck import _write_input_deck as write_input_deck
from .Legacy.trunk.S.Methods.Aerodynamics.AVL.write_run_cases import _write_run_cases as write_run_cases
from .Legacy.trunk.S.Methods.Aerodynamics.AVL.write_avl_airfoil_file import _write_avl_airfoil_file as write_avl_airfoil_file
from . import _Data as Data
