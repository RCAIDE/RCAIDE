# RCAIDE/Methods/Aerodynamics/Common/Drag/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

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

from .parasite_drag_wing                        import parasite_drag_wing
from .parasite_drag_pylon                       import parasite_drag_pylon
from .parasite_total                            import parasite_total
from .induced_drag                              import induced_drag
from .wave_drag                                 import wave_drag 
from .lift_wave_drag                            import lift_wave_drag 
from .parasite_drag_fuselage                    import parasite_drag_fuselage
from .compressibility_drag                      import compressibility_drag
from .miscellaneous_drag                        import miscellaneous_drag  
from .parasite_drag_nacelle                     import parasite_drag_nacelle   
from .spoiler_drag                              import spoiler_drag 
from .wave_drag                                 import wave_drag 
from .total_drag                                import total_drag 
from .supersonic_wave_drag_volume_raymer        import supersonic_wave_drag_volume_raymer
from .supersonic_wave_drag_volume_sears_haack   import supersonic_wave_drag_volume_sears_haack