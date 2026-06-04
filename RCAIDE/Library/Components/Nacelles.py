# $NAME.py
# (c) Copyright 2025 Aerospace Research Community LLC
#
# Created: Apr 2025, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# package imports
import equinox as eqx
import jax.numpy as jnp

# RCAIDE imports
from RCAIDE.Library import Component, ComponentDimensions

# ----------------------------------------------------------------------------------------------------------------------
#  Nacelle
# ----------------------------------------------------------------------------------------------------------------------


class NacelleDiameters(ComponentDimensions):

    inlet: float = 0.0


class Nacelle(Component):

    tag:                        str     = eqx.field(static=True, default='Nacelle')
    flow_through:               bool    = eqx.field(static=True, default=False)
    fuselage_integrated:        bool    = eqx.field(static=True, default=False)
    has_pylon:                  bool    = eqx.field(default=True)

    aerodynamic_center:         jnp.ndarray         = eqx.field(default_factory=lambda: jnp.empty((0, 3)))
    orientation_euler_angles:   jnp.ndarray         = eqx.field(default_factory=lambda: jnp.empty((0, 3)))

    airfoil:                    Component | None    = None
    cowling_airfoil_angle:      float               = 0.0

    diameters:                  NacelleDiameters = eqx.field(default_factory=NacelleDiameters) #type: ignore
