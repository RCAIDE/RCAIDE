## @defgroup Library-Methods-Aerdoynamics-Common-Drag Drag 
# @ingroup Library-Methods-Aerdoynamics-Common
# RCAIDE/Methods/Aerodynamics/Common/Drag/__init__.py
# 

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

from .parasite_drag_wing                    import parasite_drag_wing
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Drag.parasite_drag_fuselage                import parasite_drag_fuselage
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Drag.parasite_drag_nacelle                 import parasite_drag_nacelle
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Drag.parasite_drag_pylon                   import parasite_drag_pylon
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Drag.parasite_total                        import parasite_total
from .induced_drag_aircraft                 import induced_drag_aircraft
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Drag.compressibility_drag_wing             import compressibility_drag_wing
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Drag.compressibility_drag_wing_total       import compressibility_drag_wing_total
from .miscellaneous_drag_aircraft_ESDU                                                                   import miscellaneous_drag_aircraft_ESDU
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Drag.trim                                  import trim
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Drag.spoiler_drag                          import spoiler_drag
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Drag.untrimmed                             import untrimmed
from Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Drag.total_aircraft                        import total_aircraft 
from Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.wave_drag_volume_raymer                    import wave_drag_volume_raymer
from Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.wave_drag_volume_sears_haack               import wave_drag_volume_sears_haack
from .compressibility_drag_total                 import compressibility_drag_total
from Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.parasite_drag_nacelle                      import parasite_drag_nacelle as supersonic_nacelle_drag_fuselage
from .wave_drag                            import wave_drag 
from Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.parasite_drag_fuselage                     import parasite_drag_fuselage as supersonic_parasite_drag_fuselage
from Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.miscellaneous_drag_aircraft                import miscellaneous_drag_aircraft