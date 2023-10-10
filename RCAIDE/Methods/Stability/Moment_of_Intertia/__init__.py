## @defgroup Methods-Stability-Moment_of_Intertia
# RCAIDE/Methods/Stability/Moment_of_Intertia/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

"""RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .compute_vehicle_moment_of_inertia    import compute_vehicle_moment_inertia
from .compute_component_moments_of_inertia import calculate_moment_of_inertia_cuboid
from .compute_component_moments_of_inertia import calculate_moment_of_inertia_hollow_cuboid 