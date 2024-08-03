# RCAIDE/Framework/Conditions/AeroDerivatives.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field

# package imports
import numpy as np

# RCAIDE imports
from RCAIDE.Framework.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  AeroDerivatives
# ----------------------------------------------------------------------------------------------------------------------

@dataclasses(kw_only=True)
class AeroDerivativesConditions(Conditions):

    name: str = 'Aerodynamic Derivatives'



    
