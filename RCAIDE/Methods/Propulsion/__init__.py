## @defgroup Methods-Propulsion Propulsion
# RCAIDE/Methods/Propulsion/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .                                                                        import Rotor_Wake
from .                                                                        import Rotor_Design
from Legacy.trunk.S.Methods.Propulsion.ducted_fan_sizing                      import ducted_fan_sizing
from .design_propeller                                                        import design_propeller 
from .design_lift_rotor                                                       import design_lift_rotor
from .design_prop_rotor                                                       import design_prop_rotor 
from Legacy.trunk.S.Methods.Propulsion.turbofan_emission_index                import turbofan_emission_index
from .size_electric_motor                                                     import size_from_kv, size_from_mass, size_optimal_motor
from .all_electric_propulsor                                                  import compute_propulsor_performance , compute_unique_propulsor_groups
from .internal_combustion_engine_cs_propulsor                                 import compute_propulsor_performance , compute_unique_propulsor_groups
from .internal_combustion_engine_propulsor                                    import compute_propulsor_performance , compute_unique_propulsor_groups
from Legacy.trunk.S.Methods.Propulsion.turbofan_sizing                        import turbofan_sizing
from Legacy.trunk.S.Methods.Propulsion.turbojet_sizing                        import turbojet_sizing
from Legacy.trunk.S.Methods.Propulsion.ramjet_sizing                          import ramjet_sizing
from Legacy.trunk.S.Methods.Propulsion.scramjet_sizing                        import scramjet_sizing
from Legacy.trunk.S.Methods.Propulsion.fm_id                                  import fm_id
from Legacy.trunk.S.Methods.Propulsion.fm_solver                              import fm_solver
from Legacy.trunk.S.Methods.Propulsion.rayleigh                               import rayleigh
from Legacy.trunk.S.Methods.Propulsion.nozzle_calculations                    import exit_Mach_shock, mach_area, normal_shock, pressure_ratio_isentropic, pressure_ratio_shock_in_nozzle
from Legacy.trunk.S.Methods.Propulsion                                        import electric_motor_sizing
from Legacy.trunk.S.Methods.Propulsion.liquid_rocket_sizing                   import liquid_rocket_sizing
from Legacy.trunk.S.Methods.Propulsion.serial_HTS_turboelectric_sizing        import serial_HTS_turboelectric_sizing
from Legacy.trunk.S.Methods.Propulsion.serial_HTS_dynamo_turboelectric_sizing import serial_HTS_dynamo_turboelectric_sizing
 