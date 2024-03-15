## @defgroup Framework-Methods-Aerodynamics-Common " + f"Drag
# RCAIDE/Library/Methods/Aerodynamics/Common/Drag/__init__.py
#

"""RCAIDE Framework Package Setup.
"""
# ------------------------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------------------------
# @ingroup Methods-Aerodynamics-Common

from .Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Drag.parasite_drag_wing import _parasite_drag_wing as parasite_drag_wing
from .Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Drag.parasite_drag_fuselage import _parasite_drag_fuselage as parasite_drag_fuselage
from .Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Drag.parasite_drag_nacelle import _parasite_drag_nacelle as parasite_drag_nacelle
from .Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Drag.parasite_drag_pylon import _parasite_drag_pylon as parasite_drag_pylon
from .Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Drag.parasite_total import _parasite_total as parasite_total
from .induced_drag_aircraft import _induced_drag_aircraft as induced_drag_aircraft
from .Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Drag.compressibility_drag_wing import _compressibility_drag_wing as compressibility_drag_wing
from .Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Drag.compressibility_drag_wing_total import _compressibility_drag_wing_total as compressibility_drag_wing_total
from .miscellaneous_drag_aircraft_ESDU import _miscellaneous_drag_aircraft_ESDU as miscellaneous_drag_aircraft_ESDU
from .Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Drag.trim import _trim as trim
from .Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Drag.spoiler_drag import _spoiler_drag as spoiler_drag
from .Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Drag.untrimmed import _untrimmed as untrimmed
from .Legacy.trunk.S.Methods.Aerodynamics.Common.Fidelity_Zero.Drag.total_aircraft import _total_aircraft as total_aircraft
from .Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.wave_drag_volume_raymer import _wave_drag_volume_raymer as wave_drag_volume_raymer
from .Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.wave_drag_volume_sears_haack import _wave_drag_volume_sears_haack as wave_drag_volume_sears_haack
from .compressibility_drag_total import _compressibility_drag_total as compressibility_drag_total
from .Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.parasite_drag_nacelle import _parasite_drag_nacelle as parasite_drag_nacelle
from .wave_drag import _wave_drag as wave_drag
from .Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.parasite_drag_fuselage import _parasite_drag_fuselage as parasite_drag_fuselage
from .Legacy.trunk.S.Methods.Aerodynamics.Supersonic_Zero.Drag.miscellaneous_drag_aircraft import _miscellaneous_drag_aircraft as miscellaneous_drag_aircraft
