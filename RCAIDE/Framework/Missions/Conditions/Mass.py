# RCAIDE/Framework/Missions/Conditions/Mass.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field

# package imports
import numpy as np

# RCAIDE imports
from RCAIDE.Framework.Missions.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Mass
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class MassConditions(Conditions):
    """
    Represents the mass conditions for a vehicle or system.

    This class extends the Conditions base class to specifically handle mass-related
    parameters and calculations.

    Attributes
    ----------
    name : str
        The name of the mass conditions.

    total : np.ndarray
        The total mass of the system.
    rate_of_change : np.ndarray
        The rate of change of mass.

    total_moment_of_inertia : np.ndarray
        The total moment of inertia.

    breakdown : Conditions
        A nested Conditions object representing the breakdown of mass components.

    Notes
    -----
    All attributes are initialized using default factories to ensure each instance
    has its own copy of mutable objects.
    """

    name:                       str         = 'Mass Conditions'

    total:                      np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))
    rate_of_change:             np.ndarray  = field(default_factory=lambda: np.zeros((1, 1)))

    total_moment_of_inertia:    np.ndarray  = field(default_factory=lambda: np.zeros((1, 3)))

    breakdown:                  Conditions  = Conditions(name='Mass Breakdown')
