## @defgroup Methods-Energy-Propulsion-Converters-Motor 
# RCAIDE/Methods/Energy/Propulsion/Converters/Motor/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
  
from .design_electric_motor              import size_from_kv, size_from_mass, size_optimal_motor  
from Legacy.trunk.S.Methods.Propulsion   import electric_motor_sizing