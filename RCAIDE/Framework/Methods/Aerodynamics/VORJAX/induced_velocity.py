# RCAIDE/Framework/Methods/Aerodynamics/VLM/induced_velocity.py
# (c) Copyright 2026 Aerospace Research Community LLC
#
# Created: Mar 2026, J. Smart
# Modified: Mar 2026, J. Smart

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from typing import TYPE_CHECKING

import jax
import jax.numpy as jnp
import equinox as eqx

# --- Framework Imports (Strictly for Type Hinting to avoid Circular Imports) ---
if TYPE_CHECKING:
    from RCAIDE.Framework.State import State
    from RCAIDE.Framework.System import System
    from RCAIDE.Framework.Settings import Settings

from RCAIDE.utils import inputs, outputs
# ----------------------------------------------------------------------------------------------------------------------
#  Helper Functions
# ----------------------------------------------------------------------------------------------------------------------


@jax.jit
def subsonic_induction(z, x1_sq, r_o1, x2_sq, r_o2, x_ty, t, B_sq, z_sq, tol_sq, x1, y1, x2, y2, r_tv1, r_tv2):
    """
    Pure JAX translation of the VORLAX subsonic Biot-Savart induction.

    This kernel computes the induced velocity (U, V, W) at a collocation point
    due to a single swept horseshoe vortex, applying local compressibility scaling.

    Variable Glossary (Miranda-Elliott-Baker Local Swept Coordinate System):
    -------------------------------------------------------------------------
    z               : Vertical distance from the collocation point to the vortex plane.
    x1, x2          : Streamwise distances from the collocation pt to vortex endpoints 1 and 2.
    y1, y2          : Spanwise distances from the collocation pt to vortex endpoints 1 and 2.
    x_sq1, x_sq2    : Squared streamwise distances (X1^2, X2^2).
    r_tv1, r_tv2    : Squared transverse distances (Y^2 + Z^2) to endpoints.
    beta_sq         : Compressibility factor (M^2 - 1). Negative in subsonic flow.
    r_o1, r_o2      : Compressibility-scaled transverse distances (B2 * RTV).
    r1, r2          : "Effective" compressible distances to endpoints sqrt(X^2 - B^2 * RTV^2).
    t               : Tangent of the bound vortex sweep angle.
    x_ty            : Cross-term projection mapping the distance along the swept vortex line.
    tol_sq          : Squared singularity tolerance (prevents div-by-zero near the filament).
    F_b2, F_b2      : Bound vortex influence terms.
    F_t1, F_t2      : Trailing vortex influence terms.
    """
    C_pi = 4.0 * jnp.pi

    # 1. Effective Compressible Distances
    # Using 1e-16 prevents exact 0.0 which would cause NaN gradients in downstream divisions
    r1 = jnp.sqrt(jnp.maximum(x1_sq - r_o1, 1e-16))
    r2 = jnp.sqrt(jnp.maximum(x2_sq - r_o2, 1e-16))

    # 2. Bound Vortex Denominator
    t_Bz = (jnp.square(t) - B_sq) * z_sq
    safe_denom = jnp.maximum(jnp.square(x_ty) + t_Bz, tol_sq)

    # 3. DRY Helper Function with NaN-safe division
    def calc_F(x, y, r, r_tv):
        # F_b: Influence contribution from the bound (swept) segment
        F_b = (t * x - B_sq * y) / r

        # F_t: Influence contribution from the semi-infinite trailing leg
        # safe_denom prevents divide-by-zero in the unselected jnp.where branch
        safe_denom = jnp.where(r_tv < tol_sq, 1.0, r * r_tv)
        F_t = jnp.where(r_tv < tol_sq, 0.0, (x + r) / safe_denom)

        return F_b, F_t

    # Evaluate for Endpoint 1 (Left/A) and Endpoint 2 (Right/B)
    F_b1, F_t1 = calc_F(x1, y1, r1, r_tv1)
    F_b2, F_t2 = calc_F(x2, y2, r2, r_tv2)

    # 4. Final Velocity Assembly
    Q_b = (F_b1 - F_b2) / safe_denom
    z_pi = z / C_pi

    # U: Streamwise induced velocity (Perturbation velocity)
    U = jnp.where(z_sq < tol_sq, 0.0, z_pi * Q_b)

    # V: Spanwise induced velocity (Sidewash)
    V = jnp.where(z_sq < tol_sq, 0.0, z_pi * (F_t1 - F_t2 - Q_b * t))

    # W: Normal induced velocity (Downwash)
    W = -(Q_b * x_ty + F_t1 * y1 - F_t2 * y2) / C_pi

    return U, V, W


@jax.jit
def supersonic_in_plane(r1, r2, y1, y2, tol, x_ty, C_pi):
    """
    Pure JAX translation of the in-plane supersonic induction.
    Evaluates downwash analytically when the collocation point sits exactly
    in the Z=0 plane of the vortex (where RTV -> 0).
    """
    # AD-Safe Denominators (Prevents NaN gradients in unselected branches)
    safe_Y1 = jnp.where(jnp.abs(y1) > tol, y1, 1.0)
    safe_Y2 = jnp.where(jnp.abs(y2) > tol, y2, 1.0)
    safe_XTY = jnp.where(jnp.abs(x_ty) > tol, x_ty, 1.0)

    F1 = jnp.where(jnp.abs(y1) > tol, r1 / safe_Y1, 0.0)
    F2 = jnp.where(jnp.abs(y2) > tol, r2 / safe_Y2, 0.0)

    W_in = jnp.where(jnp.abs(x_ty) > tol, (-F1 + F2) / (safe_XTY * C_pi), 0.0)
    return W_in


@jax.jit
def supersonic_induction(z, x_sq1, r_o1, x_sq2, r_o2, x_ty, t, B_sq, z_sq, tol_sq, tol, tol_sq2, x1, y1, x2, y2, r_tv1, r_tv2,
                         c, sonic_mask, recv_idx):
    """
    Pure JAX translation of the VORLAX supersonic Biot-Savart induction.

    Variable Glossary (Supersonic Additions):
    -------------------------------------------------------------------------
    cutoff     : Defines the boundary of the Mach cone interaction.
    reps       : Mach cone proximity threshold.
    valid1/2   : Boolean masks. True if the point lies inside the downstream Mach cone.
    WWAVE      : The Principal Part of the singular integral. Represents the 2D wave
                 drag contribution of the panel on itself (self-induction).
    T2A / T2F  : Aft and Forward panel sweep tangents, used to detect sonic edges.
    TRANS      : Edge condition parameter. If TRANS < 0, the edge is "sonic"
                 (sweep angle exactly matches the Mach angle).
    RFLAG      : Subsonic/Supersonic leading edge flag used downstream for LE suction.
    sonic_mask : Identifies panels exhibiting mathematical singularities at Mach=sec(sweep).
    """
    C_pi = 2.0 * jnp.pi
    t_sq = jnp.square(t)
    z_pi = z / C_pi
    cutoff = 0.8

    # Mach Cone Distances (Real only inside the cone)
    r1 = jnp.where(x_sq1 > r_o1, jnp.sqrt(jnp.maximum(x_sq1 - r_o1, 1e-16)), 0.0)
    r2 = jnp.where(x_sq2 > r_o2, jnp.sqrt(jnp.maximum(x_sq2 - r_o2, 1e-16)), 0.0)

    # Denominator Setup
    safe_denom = jnp.square(x_ty) + (t_sq - B_sq) * z_sq
    sgn = jnp.where(safe_denom < 0, -1.0, 1.0)
    safe_denom = jnp.where(jnp.abs(safe_denom) < tol_sq, sgn * tol_sq, safe_denom)

    def calc_F(x, y, x_sq, r_o, r, r_tv):
        reps = cutoff * x_sq
        valid = (x >= tol) & (r != 0.0) & (r_o <= reps) & (r_tv >= tol_sq)

        # AD-Safe denominators (only applied when 'valid' is True)
        safe_r = jnp.where(valid, r, 1.0)
        safe_rr_tv = jnp.where(valid, r * r_tv, 1.0)

        # 1.0 fallback is mathematically required by VORLAX supersonic integration
        F_b = jnp.where(valid, (t * x - B_sq * y) / safe_r, 1.0)
        F_t = jnp.where(valid, x / safe_rr_tv, 1.0)

        return F_b, F_t

    F_b1, F_t1 = calc_F(x1, y1, x_sq1, r_o1, r1, r_tv1)
    F_b2, F_t2 = calc_F(x2, y2, x_sq2, r_o2, r2, r_tv2)

    # Global Velocity Assembly
    Q_b = (F_b1 - F_b2) / safe_denom
    U = z_pi * Q_b
    V = z_pi * (F_t1 - F_t2 - Q_b * t)
    W = -(Q_b * x_ty + F_t1 * y1 - F_t2 * y2) / C_pi

    # In-Plane Singularity Override
    in_plane = z_sq < tol_sq2
    W_in = supersonic_in_plane(r1, r2, y1, y2, tol, x_ty, C_pi)

    U = jnp.where(in_plane, 0.0, U)
    V = jnp.where(in_plane, 0.0, V)
    W = jnp.where(in_plane, W_in, W)

    # W_wave: Principal Part of the Integral (Self-Influence / Wave Drag)
    N = U.shape[1]
    t_sq = t ** 2
    cos_sweep = 1.0 / jnp.sqrt(1.0 + t_sq[None, :])

    W_wave_cond = B_sq > t_sq[None, :]
    W_wave_output = -0.5 * jnp.sqrt(jnp.where(W_wave_cond, B_sq - t_sq[None, :], 1.0)) / jnp.maximum(c, 1e-12)

    # Calculate W_wave for all senders (Shape: n_time, N)
    W_wave_val = jnp.where(
        W_wave_cond,
        W_wave_output,
        0.0
    )

    # Create a boolean mask for the diagonal element of this specific row
    j_indices = jnp.arange(N)
    is_diag = (j_indices == recv_idx)[None, :]

    # Only add the W_wave value to the element where sender == receiver
    W = W + jnp.where(is_diag, W_wave_val, 0.0)

    # Build the 1D slice of the Laplacian stencil for THIS receiver row
    sonic_row = jnp.where(
        j_indices == recv_idx, 2.0,
        jnp.where(j_indices == recv_idx - 1, -1.0,
        jnp.where(j_indices == recv_idx + 1, -1.0, 0.0))
    )[None, :]

    is_recv_sonic = sonic_mask[:, recv_idx][:, None]

    # Overwrite the influence of sonic sending panels with the smoothing stencil
    W = jnp.where(is_recv_sonic, sonic_row, W)

    return U, V, W

@jax.jit
@jax.checkpoint
def compute_C_ij(VD, Mach):
    """
    Computes the Aerodynamic Influence Coefficient matrix C_ij.
    Output Shape: (n_time, N, N, 3)
    """

    # Unpack Vortex Distribution Data ----------------------------------------------------------------------------------
    vortex_A = VD.bound_vortex_A.astype(jnp.float32)
    vortex_B = VD.bound_vortex_B.astype(jnp.float32)
    center = VD.bound_vortex_center.astype(jnp.float32)
    colloc = VD.collocation_points.astype(jnp.float32)

    # Local Panel Orientation ------------------------------------------------------------------------------------------
    dy = vortex_B[:, 1] - vortex_A[:, 1]
    dz = vortex_B[:, 2] - vortex_A[:, 2]

    norm_yz = jnp.maximum(jnp.sqrt(dy ** 2 + dz ** 2), 1e-16)
    costheta = dy / norm_yz
    sintheta = dz / norm_yz

    # Local Panel Sweep ------------------------------------------------------------------------------------------------
    dx_vortex = vortex_B[:, 0] - center[:, 0]
    dy_vortex = (vortex_B[:, 1] - center[:, 1]) * costheta + (vortex_B[:, 2] - center[:, 2]) * sintheta

    # s = local half-span, t = tangent of the sweep angle
    s = jnp.abs(dy_vortex)
    t = (dx_vortex / jnp.maximum(dy_vortex, 1e-16))
    t_sq = t ** 2

    # Beta-Squared = Mach^2 - 1.0 --------------------------------------------------------------------------------------
    beta_sq = (Mach.squeeze(1) ** 2 - 1.0).astype(jnp.float32)
    beta_sq_exp = beta_sq[:, None] if beta_sq.ndim == 1 else beta_sq
    is_subsonic = beta_sq_exp < 0.0

    # Sonic Mask Pre-Calc ----------------------------------------------------------------------------------------------
    t_sq_fore = jnp.where(VD.is_leading_edge, 0.0, jnp.roll(t_sq, shift=1))
    t_sq_aft = jnp.where(VD.is_trailing_edge, 0.0, jnp.roll(t_sq, shift=-1))

    sonic_check = (beta_sq_exp - t_sq_fore[None, :]) * (beta_sq_exp - t_sq_aft[None, :])
    sonic_mask = (sonic_check < 0) & VD.is_leading_edge

    # Check for singularity (Mach cone passes through panel)
    singularity_flag = jnp.where(sonic_mask, 0, 1)
    singularity_flag = jnp.where(is_subsonic, 1, singularity_flag)

    safe_beta_sq = jnp.maximum(t_sq_fore[None, :], t_sq_aft[None, :]) + 0.01
    beta_sq_exp = jnp.where(sonic_mask, safe_beta_sq, beta_sq_exp)

    # C_mn Calculation -------------------------------------------------------------------------------------------------

    tol = s / 500.0
    tol_sq = tol ** 2
    tol_sq_scl = 2500.0 * tol_sq

    # Row-wise vector-mapping to minimize peak memory usage
    def compute_row(c_pt, ct_R, st_R, recv_idx):
        dx = c_pt[0] - center[:, 0]
        dy = c_pt[1] - center[:, 1]
        dz = c_pt[2] - center[:, 2]

        y_dist = dy * costheta + dz * sintheta
        z_dist = -dy * sintheta + dz * costheta

        x_dist_left = dx + t * s
        x_dist_right = dx - t * s
        x_dist_center = dx - t * y_dist

        y_dist_left = y_dist + s
        y_dist_right = y_dist - s

        # Arrays are (N,) instead of (N, N)
        x_sq1 = x_dist_left ** 2
        x_sq2 = x_dist_right ** 2
        y_sq1 = y_dist_left ** 2
        y_sq2 = y_dist_right ** 2
        z_sq  = z_dist ** 2

        r_tv1 = y_sq1 + z_sq
        r_tv2 = y_sq2 + z_sq

        # Broadcast the Mach/Time dimension here: (n_time, 1) * (N,) -> (n_time, N)
        r_o1 = beta_sq_exp * r_tv1[None, :]
        r_o2 = beta_sq_exp * r_tv2[None, :]

        # --- Subsonic Kernel ---
        U_ind, V_ind, W_ind = subsonic_induction(
            x1_sq=x_sq1,
            x2_sq=x_sq2,
            x_ty=x_dist_center,
            x1=x_dist_left,
            x2=x_dist_right,
            y1=y_dist_left,
            y2=y_dist_right,
            z=z_dist,
            z_sq=z_sq,
            r_tv1=r_tv1,
            r_tv2=r_tv2,
            r_o1=r_o1,
            r_o2=r_o2,
            t=t,
            B_sq=beta_sq_exp,
            tol_sq=tol_sq,
        )

        # --- Supersonic Kernel ---
        U_sup, V_sup, W_sup = supersonic_induction(
            x_sq1=x_sq1,
            x_sq2=x_sq2,
            x_ty=x_dist_center,
            x1=x_dist_left,
            x2=x_dist_right,
            y1=y_dist_left,
            y2=y_dist_right,
            z=z_dist,
            z_sq=z_sq,
            r_tv1=r_tv1,
            r_tv2=r_tv2,
            r_o1=r_o1,
            r_o2=r_o2,
            t=t,
            B_sq=beta_sq_exp,
            tol=tol,
            tol_sq=tol_sq,
            tol_sq2=tol_sq_scl,
            c=VD.chord_lengths,
            sonic_mask=sonic_mask,
            recv_idx=recv_idx
        )

        # --- Blending ---
        U_ind = jnp.where(is_subsonic, U_ind, U_sup)
        V_ind = jnp.where(is_subsonic, V_ind, V_sup)
        W_ind = jnp.where(is_subsonic, W_ind, W_sup)

        # --- EW Calculation ---
        # Note: ct_S and st_S are just the global 'costheta' and 'sintheta' arrays
        COS_RS = ct_R * costheta + st_R * sintheta
        SIN_RS = st_R * costheta - ct_R * sintheta


        EW_row = W_ind * COS_RS[None, :] - V_ind * SIN_RS[None, :]

        # --- Rotate to Global Frame ---
        C_ij_row = jnp.stack([
                U_ind,
                V_ind * costheta[None, :] - W_ind * sintheta[None, :],
                V_ind * sintheta[None, :] + W_ind * costheta[None, :]
            ], axis=-1)

        # Return the tuple!
        return C_ij_row, EW_row

    C_ij_mapped, _ = jax.vmap(compute_row)(colloc, costheta, sintheta, jnp.arange(VD.total_panels))
    C_mn = jnp.swapaxes(C_ij_mapped, 0, 1)
    
    # If using chordwise cosine spacing, compute leading edge normalwash for Lan's method
    # (Currently unsupported, commented out to minimize memory footprint)

    # front_left = VD.panel_vertices[:, 0, :]
    # front_right = VD.panel_vertices[:, 3, :]
    # front_mid = 0.5 * (front_left + front_right)

    # _, LN_mapped = jax.vmap(compute_row)(front_mid, costheta, sintheta, jnp.arange(VD.total_panels))
    # LN = jnp.swapaxes(LN_mapped, 0, 1)

    return C_mn.astype(jnp.float64), singularity_flag

    
# ----------------------------------------------------------------------------------------------------------------------
#  Wing Induced Velocity Calculation
# ----------------------------------------------------------------------------------------------------------------------


@inputs(
    "system.analysis_data['vortex_distribution']",
    "state.freestream.mach_number"
)
@outputs(
    "system.analysis_data['VICs']",
    "system.analysis_data['singularities']",
    "system.analysis_data['le_normalwash']"
)
def compute_induced_velocity(state: "State", system: "System", settings: "Settings"):
    
    VD = system.analysis_data["vortex_distribution"]
    Mach = state.freestream.mach_number
    
    C_ij, singularity_flag, = compute_C_ij(VD, Mach)
    
    updated_analysis_data = system.analysis_data | {
        "VICs": C_ij,
        "singularities": singularity_flag,
    }

    updated_system = eqx.tree_at(lambda s: s.analysis_data, system, updated_analysis_data)
    
    return state, updated_system, settings
