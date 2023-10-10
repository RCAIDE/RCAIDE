## @defgroup Methods-Weights-Center_of_Gravity Center_of_Gravity
# RCAIDE/Methods/Weights/Center_of_Gravity/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

"""RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from .compute_vehicle_center_of_gravity                                                         import compute_vehicle_center_of_gravity
from .compute_component_centers_of_gravity                                                      import compute_component_centers_of_gravity
from Legacy.trunk.S.Methods.Center_of_Gravity.compute_mission_center_of_gravity                 import compute_mission_center_of_gravity
from Legacy.trunk.S.Methods.Center_of_Gravity.compute_fuel_center_of_gravity_longitudinal_range import compute_fuel_center_of_gravity_longitudinal_range