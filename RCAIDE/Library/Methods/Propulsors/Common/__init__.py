## @defgroup Methods-Energy-Propulsion-Converters-Common Common 
# RCAIDE/Methods/Energy/Propulsion/Converters/Common/__init__.py
# 

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .compute_static_sea_level_performance                                    import compute_static_sea_level_performance
from .append_avionics_conditions                                              import append_avionics_conditions
from .append_payload_conditions                                               import append_payload_conditions

from Legacy.trunk.S.Methods.Propulsion.fm_id                                  import fm_id
from Legacy.trunk.S.Methods.Propulsion.fm_solver                              import fm_solver
from Legacy.trunk.S.Methods.Propulsion.rayleigh                               import rayleigh
from Legacy.trunk.S.Methods.Propulsion.nozzle_calculations                    import exit_Mach_shock, mach_area, normal_shock, pressure_ratio_isentropic, pressure_ratio_shock_in_nozzle 