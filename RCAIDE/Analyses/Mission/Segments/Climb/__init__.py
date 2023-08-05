## @defgroup Analyses-Mission-Segments-Climb Climb
# RCAIDE/Analyses/Mission/Segments/Climb/__init__.py
# (c) Copyright 2023 Aerospace Research Community LLC

"""RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from Legacy.trunk.S.Analyses.Mission.Segments.Climb.Constant_Dynamic_Pressure_Constant_Angle import Constant_Dynamic_Pressure_Constant_Angle
from Legacy.trunk.S.Analyses.Mission.Segments.Climb.Constant_Dynamic_Pressure_Constant_Rate  import Constant_Dynamic_Pressure_Constant_Rate
from Legacy.trunk.S.Analyses.Mission.Segments.Climb.Constant_Mach_Constant_Angle             import Constant_Mach_Constant_Angle
from Legacy.trunk.S.Analyses.Mission.Segments.Climb.Constant_Mach_Constant_Rate              import Constant_Mach_Constant_Rate
from Legacy.trunk.S.Analyses.Mission.Segments.Climb.Constant_Mach_Linear_Altitude            import Constant_Mach_Linear_Altitude
from Legacy.trunk.S.Analyses.Mission.Segments.Climb.Constant_Speed_Constant_Angle            import Constant_Speed_Constant_Angle
from Legacy.trunk.S.Analyses.Mission.Segments.Climb.Constant_Speed_Constant_Angle_Noise      import Constant_Speed_Constant_Angle_Noise
from Legacy.trunk.S.Analyses.Mission.Segments.Climb.Constant_Speed_Constant_Rate             import Constant_Speed_Constant_Rate
from Legacy.trunk.S.Analyses.Mission.Segments.Climb.Constant_Speed_Linear_Altitude           import Constant_Speed_Linear_Altitude
from Legacy.trunk.S.Analyses.Mission.Segments.Climb.Constant_Throttle_Constant_Speed         import Constant_Throttle_Constant_Speed
from Legacy.trunk.S.Analyses.Mission.Segments.Climb.Linear_Mach_Constant_Rate                import Linear_Mach_Constant_Rate
from Legacy.trunk.S.Analyses.Mission.Segments.Climb.Linear_Speed_Constant_Rate               import Linear_Speed_Constant_Rate
from Legacy.trunk.S.Analyses.Mission.Segments.Climb.Constant_EAS_Constant_Rate               import Constant_EAS_Constant_Rate
from Legacy.trunk.S.Analyses.Mission.Segments.Climb.Constant_CAS_Constant_Rate               import Constant_CAS_Constant_Rate
from Legacy.trunk.S.Analyses.Mission.Segments.Climb.Optimized                                import Optimized
from Legacy.trunk.S.Analyses.Mission.Segments.Climb.Unknown_Throttle                         import Unknown_Throttle