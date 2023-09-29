
## @defgroup Methods-Thermal_Management-Battery-Channel_Cooling
# @ingroup Methods

from .                                            import Sizing
from .channel_cooling_model                       import compute_net_generated_battery_heat_chan
from .channel_cooling_model                       import compute_net_generated_battery_heat_hex  
from .compute_heat_exhanger_factors               import compute_heat_exhanger_factors
from .compute_heat_exhanger_offdesign_performance import compute_offdesign_pressure_properties
from .compute_heat_exhanger_offdesign_performance import compute_offdesign_thermal_properties
from .compute_heat_exhanger_offdesign_performance import compute_surface_geometry_properties
from .compute_heat_exhanger_offdesign_performance import compute_offdesign_geometry