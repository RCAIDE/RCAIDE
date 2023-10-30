## @defgroup Methods-Aerodynamics Aerodynamics 
# RCAIDE/Methods/Aerodynamics/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from . import Airfoil_Panel_Method
from .compute_airfoil_properties_from_polar_files import compute_airfoil_properties_from_polar_files
from .compute_airfoil_properties_from_panel_method import compute_airfoil_properties_from_panel_method
from .import_airfoil_geometry import import_airfoil_geometry