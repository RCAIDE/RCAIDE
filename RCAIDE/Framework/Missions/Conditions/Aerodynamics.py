# RCAIDE/Framework/Missions/Conditions/Aerodynamics.py
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
from RCAIDE.Framework.Missions.Conditions import Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Aerodynamics
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class DragBreakdown(Conditions):

    #Attribute          Type        Default Value
    name:               str         = 'Drag Breakdown'

    parasite:           Conditions  = Conditions(name='Parasite Drag')
    compressibility:    Conditions  = Conditions(name='Compressibility Drag')
    induced:            Conditions  = Conditions(name='Induced Drag')


@dataclass(kw_only=True)
class AerodynamicsConditions(Conditions):

    #Attribute          Type            Default Value
    name:               str             = 'Aerodynamics'

    angle_of_attack:    np.ndarray      = field(default_factory=lambda: np.zeros((1, 1)))
    side_slip_angle:    np.ndarray      = field(default_factory=lambda: np.zeros((1, 1)))
    roll_angle:         np.ndarray      = field(default_factory=lambda: np.zeros((1, 1)))
    lift_coefficient:   np.ndarray      = field(default_factory=lambda: np.zeros((1, 1)))
    drag_coefficient:   np.ndarray      = field(default_factory=lambda: np.zeros((1, 1)))

    lift_breakdown:     Conditions      = Conditions(name='Lift Breakdown')
    drag_breakdown:     DragBreakdown   = DragBreakdown()
