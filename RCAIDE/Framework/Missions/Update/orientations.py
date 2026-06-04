# RCAIDE/Framework/Missions/Update/orientations.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Aug 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# package imports
import equinox as eqx
import jax.numpy as jnp
from jax import vmap

# RCAIDE imports
import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
#  Update Orientations
# ----------------------------------------------------------------------------------------------------------------------

import jax.numpy as jnp


def euler_zyx_to_dcm(angles):
    """
    Converts a single [z, y, x] Euler angle array to a 3x3 rotation matrix.
    Pure JAX equivalent to SciPy's Rotation.from_euler('zyx', angles).as_matrix()
    """
    z, y, x = angles[0], angles[1], angles[2]
    
    cz, sz = jnp.cos(z), jnp.sin(z)
    cy, sy = jnp.cos(y), jnp.sin(y)
    cx, sx = jnp.cos(x), jnp.sin(x)
    
    row1 = jnp.array([cy*cz, cz*sx*sy - cx*sz, cx*cz*sy + sx*sz])
    row2 = jnp.array([cy*sz, cx*cz + sx*sy*sz, cx*sy*sz - cz*sx])
    row3 = jnp.array([-sy,   cy*sx,            cx*cy])
    
    return jnp.stack([row1, row2, row3])


vmap_euler_to_dcm = vmap(euler_zyx_to_dcm)


def update_orientations(state: "rcf.State",
                        system: "rcf.System",
                        settings: "rcf.Settings",
                        ):

    v_inertial = state.frames.inertial.velocity_vector

    # ---Body Frame Rotations---

    body_inertial_rotations = state.frames.body.inertial_rotations

    phi = body_inertial_rotations[:, 0, None]

    # Body Frame Transformation Matrices
    TB2I = vmap_euler_to_dcm(body_inertial_rotations)
    TI2B = jnp.swapaxes(TB2I, 1, 2)

    # Velocity Transformation
    v_body = jnp.einsum('nij,nj->ni', TI2B, v_inertial)

    # X-Z Projection of velocity
    v_xz = v_body.at[:, 1].set(0)
    v_xz_mag = jnp.sqrt(jnp.sum(v_xz **2, axis=1))

    # Angle of Attack
    alpha = jnp.arctan2(v_xz[:, 2], v_xz[:, 0])

    # Side Slip Angle
    beta = jnp.arctan2(v_body[:, 1], v_xz_mag)

    # ---Wind Frame Rotations---

    wind_body_rotations = jnp.zeros_like(body_inertial_rotations)
    wind_body_rotations = wind_body_rotations.at[:, 0].set(0.)        # No x-axis roll in wind frame
    wind_body_rotations = wind_body_rotations.at[:, 1].set(alpha)     # Theta is Angle of Attack
    wind_body_rotations = wind_body_rotations.at[:, 2].set(beta)      # Psi is Side Slip Angle

    TW2B = vmap_euler_to_dcm(wind_body_rotations)
    TW2I = jnp.matmul(TW2B, TB2I)

    # ---Pack Results---
    state = eqx.tree_at(
            lambda s: (
                s.aerodynamics.angles.alpha,
                s.aerodynamics.angles.beta,
                s.aerodynamics.angles.phi,
                s.frames.body.transform_to_inertial,
                s.frames.wind.transform_to_inertial,
                s.frames.wind.body_rotations,
            ),
            state, 
            (
                state.aerodynamics.angles.alpha.at[:, 0].set(alpha),
                state.aerodynamics.angles.beta.at[:, 0].set(beta),
                phi,
                TB2I,
                TW2I,
                wind_body_rotations
            )
        )
                   
    return state, system, settings
