## @defgroup Library-Methods-Aerdoynamics-Common-Drag Drag 
# @ingroup Library-Methods-Aerdoynamics-Common
# RCAIDE/Methods/Aerodynamics/Common/Drag/__init__.py
# 

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Helper_Functions.compressible_mixed_flat_plate     import compressible_mixed_flat_plate     as compressible_mixed_flat_plate
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Helper_Functions.windmilling_drag                  import windmilling_drag                  as windmilling_drag
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Helper_Functions.asymmetry_drag                    import asymmetry_drag                    as asymmetry_drag
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Helper_Functions.estimate_2ndseg_lift_drag_ratio   import estimate_2ndseg_lift_drag_ratio   as estimate_2ndseg_lift_drag_ratio
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Helper_Functions.compressible_turbulent_flat_plate import compressible_turbulent_flat_plate as  compressible_turbulent_flat_plate
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Helper_Functions.compressible_mixed_flat_plate     import compressible_mixed_flat_plate     as  compressible_mixed_flat_plate
from .compressibility_drag_wing             import compressibility_drag_wing
from .compressibility_drag_wing_total       import compressibility_drag_wing_total
from .miscellaneous_drag_aircraft           import miscellaneous_drag_aircraft
from .trimmed_drag                          import trimmed_drag
from .spoiler_drag                          import spoiler_drag
from .untrimmed_drag                        import untrimmed_drag
from .total_drag                            import total_drag
from .compressibility_drag_total            import compressibility_drag_total
from .wave_drag                             import wave_drag 
from .lift_wave_drag                        import lift_wave_drag
from .parasite_drag_wing                    import parasite_drag_wing
from .parasite_drag_fuselage                import parasite_drag_fuselage
from .parasite_drag_nacelle                 import parasite_drag_nacelle
from .parasite_drag_pylon                   import parasite_drag_pylon
from .parasite_total                        import parasite_total
from .induced_drag_aircraft                 import induced_drag_aircraft
from Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.wave_drag_volume_raymer                    import wave_drag_volume_raymer
from Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.wave_drag_volume_sears_haack               import wave_drag_volume_sears_haack
from Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.parasite_drag_nacelle                      import parasite_drag_nacelle as supersonic_nacelle_drag_nacelle
from Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.parasite_drag_fuselage                     import parasite_drag_fuselage as supersonic_parasite_drag_fuselage
from Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.miscellaneous_drag_aircraft                import miscellaneous_drag_aircraft as  supersonic_miscellaneous_drag_aircraft