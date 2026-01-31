# $NAME.py
# (c) Copyright 2025 Aerospace Research Community LLC
#
# Created: Apr 2025, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

import chex
from dataclasses import field

# package imports
import RNUMPY as rp

# RCAIDE imports
import RCAIDE.Library as rcl

import RCAIDE.Library as rcl

# ----------------------------------------------------------------------------------------------------------------------
#  Nacelle
# ----------------------------------------------------------------------------------------------------------------------


@chex.dataclass(kw_only=True)
class Nacelle(rcl.Component):

    tag:                        str     = 'Nacelle'

    flow_through:               bool    = False
    has_pylon:                  bool    = True
    fuselage_integrated:        bool    = False

    aerodynamic_center:         rp.ndarray              = field(default_factory=lambda: rp.zeros(3))
    orientation_euler_angles:   rp.ndarray              = field(default_factory=lambda: rp.zeros(3))

    airfoil:                    rcl.Component           = None
    cowling_airfoil_angle:      float                   = 0.0

    diameters:                  rcl.ComponentDimensions = field(default_factory=rcl.ComponentDimensions)

    def __post_init__(self):

        self.diameters.inlet = 0.0
