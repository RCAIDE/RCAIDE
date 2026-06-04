# RCAIDE/Methods/Geometry/Two_Dimensional/Cross_SectioNoneirfoil/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
from .compute_naca_4series           import compute_naca_4series 
from .compute_airfoil_properties     import compute_airfoil_properties
from Legacy.trunk.S.Methods.Geometry.Two_Dimensional.Cross_Section.Airfoil import import_airfoil_geometry  as import_airfoil_geometry 
from .import_airfoil_polars          import import_airfoil_polars
from .convert_airfoil_to_meshgrid    import convert_airfoil_to_meshgrid
from .generate_interpolated_airfoils import generate_interpolated_airfoils 