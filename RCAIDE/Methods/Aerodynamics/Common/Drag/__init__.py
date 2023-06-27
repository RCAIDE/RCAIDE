## @defgroup Methods-Aerodynamics-Common-Fidelity_Zero-Drag Drag
# Drag methods that are directly specified by analyses.
# @ingroup Methods-Aerodynamics-Common-Fidelity_Zero 

from Legacy.trunk.S.Methods.Aerodynamics.Common.Drag.parasite_drag_wing                    import parasite_drag_wing
from Legacy.trunk.S.Methods.Aerodynamics.Common.Drag.parasite_drag_fuselage                import parasite_drag_fuselage
from Legacy.trunk.S.Methods.Aerodynamics.Common.Drag.parasite_drag_nacelle                 import parasite_drag_nacelle
from Legacy.trunk.S.Methods.Aerodynamics.Common.Drag.parasite_drag_pylon                   import parasite_drag_pylon
from Legacy.trunk.S.Methods.Aerodynamics.Common.Drag.parasite_total                        import parasite_total
from Legacy.trunk.S.Methods.Aerodynamics.Common.Drag.induced_drag_aircraft                 import induced_drag_aircraft
from Legacy.trunk.S.Methods.Aerodynamics.Common.Drag.compressibility_drag_wing             import compressibility_drag_wing
from Legacy.trunk.S.Methods.Aerodynamics.Common.Drag.compressibility_drag_wing_total       import compressibility_drag_wing_total
from Legacy.trunk.S.Methods.Aerodynamics.Common.Drag.miscellaneous_drag_aircraft_ESDU      import miscellaneous_drag_aircraft_ESDU
from Legacy.trunk.S.Methods.Aerodynamics.Common.Drag.trim                                  import trim
from Legacy.trunk.S.Methods.Aerodynamics.Common.Drag.spoiler_drag                          import spoiler_drag
from Legacy.trunk.S.Methods.Aerodynamics.Common.Drag.untrimmed                             import untrimmed
from Legacy.trunk.S.Methods.Aerodynamics.Common.Drag.total_aircraft                        import total_aircraft 
from Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.wave_drag_volume_raymer      import wave_drag_volume_raymer
from Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.wave_drag_volume_sears_haack import wave_drag_volume_sears_haack
from Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.compressibility_drag_total   import compressibility_drag_total
from Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.parasite_drag_nacelle        import parasite_drag_nacelle
from Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.wave_drag_lift               import wave_drag_lift
from Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.parasite_drag_fuselage       import parasite_drag_fuselage
from Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.miscellaneous_drag_aircraft  import miscellaneous_drag_aircraft