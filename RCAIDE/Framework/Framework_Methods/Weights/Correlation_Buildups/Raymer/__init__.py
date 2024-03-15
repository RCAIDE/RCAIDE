## @defgroup Framework-Methods-Weights-Correlation_Buildups " + f"Raymer
# RCAIDE/Library/Methods/Weights/Correlation_Buildups/Raymer/__init__.py
#

"""RCAIDE Framework Package Setup.
"""
# ------------------------------------------------------------------------------
# IMPORT
# ------------------------------------------------------------------------------
# @ingroup Methods-Weights-Correlation_Buildups

from .Legacy.trunk.S.Methods.Weights.Correlations.Raymer.wing_main_raymer import _wing_main_raymer as wing_main_raymer
from .Legacy.trunk.S.Methods.Weights.Correlations.Raymer.tail import _tail_horizontal_Raymer as tail_horizontal_Raymer
from .Legacy.trunk.S.Methods.Weights.Correlations.Raymer.tail import _tail_vertical_Raymer as tail_vertical_Raymer
from .Legacy.trunk.S.Methods.Weights.Correlations.Raymer.fuselage import _fuselage_weight_Raymer as fuselage_weight_Raymer
from .Legacy.trunk.S.Methods.Weights.Correlations.Raymer.landing_gear import _landing_gear_Raymer as landing_gear_Raymer
from .Legacy.trunk.S.Methods.Weights.Correlations.Raymer.systems import _systems_Raymer as systems_Raymer
from .Legacy.trunk.S.Methods.Weights.Correlations.Raymer.prop_system import _total_prop_Raymer as total_prop_Raymer
