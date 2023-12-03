## @defgroup Methods-Propulsion-Performance Performance
# RCAIDE/Methods/Propulsion/Performance/__init__.py
# 

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from .                                                                        import Rotor_Wake 
from .all_electric_propulsor                                                  import compute_propulsor_performance , compute_unique_propulsor_groups 
from .internal_combustion_engine_cs_propulsor                                 import compute_propulsor_performance , compute_unique_propulsor_groups
from .internal_combustion_engine_propulsor                                    import compute_propulsor_performance , compute_unique_propulsor_groups 
from .solar_propulsor                                                         import compute_propulsor_performance , compute_unique_propulsor_groups 
from .turbofan_propulsor                                                      import compute_propulsor_performance  
from .turbojet_propulsor                                                      import compute_propulsor_performance , compute_unique_propulsor_groups 