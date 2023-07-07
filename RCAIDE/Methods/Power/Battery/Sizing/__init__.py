## @defgroup Methods-Power-Battery-Sizing Sizing
# RCAIDE/Methods/Power/Battery/Sizing/__init__.py
# (c) Copyright The Board of Trustees of RCAIDE

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# @ingroup Methods-Power-Battery

from .initialize_from_mass                  import initialize_from_mass
from .initialize_from_energy_and_power      import initialize_from_energy_and_power
from .initialize_from_circuit_configuration import initialize_from_circuit_configuration
from .find_mass_gain_rate                   import find_mass_gain_rate
from .find_total_mass_gain                  import find_total_mass_gain
