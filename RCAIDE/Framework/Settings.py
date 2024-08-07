# RCAIDE/Framework/Settings.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from typing import Callable
from dataclasses import dataclass, field

# package imports
import numpy as np
from scipy.optimize import fsolve

# RCAIDE imports

# ----------------------------------------------------------------------------------------------------------------------
#  Settings
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class Settings:

    name: str = 'Settings'

    # Mission Settings
    root_finder: Callable = fsolve