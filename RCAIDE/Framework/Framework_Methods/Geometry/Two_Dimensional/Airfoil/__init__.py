## @defgroup Framework-Methods-Geometry-Two_Dimensional " + f"Airfoil
# RCAIDE/Library/Methods/Geometry/Two_Dimensional/Airfoil/__init__.py
#

"""RCAIDE Framework Package Setup.
"""
# ------------------------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------------------------
# @ingroup Methods-Geometry-Two_Dimensional

from .Legacy.trunk.S.Methods.Geometry.Two_Dimensional.Cross_Section.Airfoil import _compute_naca_4series as compute_naca_4series
from .Legacy.trunk.S.Methods.Geometry.Two_Dimensional.Cross_Section.Airfoil import _compute_airfoil_properties as compute_airfoil_properties
from .Legacy.trunk.S.Methods.Geometry.Two_Dimensional.Cross_Section.Airfoil import _import_airfoil_dat as import_airfoil_dat
from .Legacy.trunk.S.Methods.Geometry.Two_Dimensional.Cross_Section.Airfoil import _import_airfoil_geometry as import_airfoil_geometry
from .Legacy.trunk.S.Methods.Geometry.Two_Dimensional.Cross_Section.Airfoil import _import_airfoil_polars as import_airfoil_polars
from .Legacy.trunk.S.Methods.Geometry.Two_Dimensional.Cross_Section.Airfoil import _convert_airfoil_to_meshgrid as convert_airfoil_to_meshgrid
