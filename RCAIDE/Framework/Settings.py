# RCAIDE/Framework/Settings.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------


import chex
from dataclasses import field
from typing import Callable

# package imports
from RNUMPY.scipy import fsolve

# RCAIDE imports

# ----------------------------------------------------------------------------------------------------------------------
#  Settings
# ----------------------------------------------------------------------------------------------------------------------


@chex.dataclass(kw_only=True)
class AnalysisSettings:

    aerodynamics: chex.dataclass = None


@chex.dataclass(kw_only=True)
class Settings:

    tag: str = 'Settings'

    # Mission Settings
    root_finder: Callable = fsolve

    analysis: AnalysisSettings = field(default_factory=lambda: AnalysisSettings())

