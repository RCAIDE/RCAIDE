# RCAIDE/Framework/Methods/Aerodynamics/panelization.py
# (c) Copyright 2026 Aerospace Research Community LLC
#
# Created:  Jun 2021, A. Blaufox
# Modified: May 2026, J. Smart

# ----------------------------------------------------------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------------------------------------------------------

import warnings
import dataclasses
from typing import TYPE_CHECKING, Optional

# package imports
import jax
import jax.numpy as jnp
import equinox as eqx

# --- Framework Imports (Strictly for Type Hinting to avoid Circular Imports) ---
if TYPE_CHECKING:
    from RCAIDE.Framework.State import State
    from RCAIDE.Framework.System import Aircraft
    from RCAIDE.Framework.Settings import Settings
    from RCAIDE.Framework.Analyses.Aerodynamics.VORJAX import VLMSettings

# package imports 
from RCAIDE.utils import inputs, outputs
from RCAIDE.Library.Components.Wings import Wing, WingSegment, WingSweeps, WingDimensions
# from RCAIDE.Library.Components.Wings import All_Moving_Surface

# ----------------------------------------------------------------------------------------------------------------------
# VortexDistribution Data Structure
# ----------------------------------------------------------------------------------------------------------------------

class VortexDistribution(eqx.Module):
    """ 
    A globally unstructured VLM mesh.
    N = total number of panels across the entire aircraft.
    """
    # --- Base Geometric State ---
    panel_vertices: jnp.ndarray     # (N, 4, 3), CCW from Front-Left
    camber_slopes: jnp.ndarray      # (N,) Camber slope at each panel
    wedge_angles: jnp.ndarray       # (N_s,) Leading edge wedge angle for supersonic correction
    
    # --- Identity & Topology (Calculated before flattening!) ---
    surface_id: jnp.ndarray         # (N,) ID of the originating wing/fuselage
    control_surface_id: jnp.ndarray # (N,) ID of the control surface (-1 for solid wing)
    is_leading_edge: jnp.ndarray    # (N,) Boolean mask
    is_trailing_edge: jnp.ndarray   # (N,) Boolean mask
    
    # --- Static Structural Integers (NOT traced by JAX) ---
    total_panels: int = eqx.field(static=True)
    total_strips: int = eqx.field(static=True)

    def __init__(self, panel_vertices, camber_slopes, wedge_angles, surface_id, control_surface_id, is_leading_edge, is_trailing_edge, total_panels=None, total_strips=None, **kwargs):
        self.panel_vertices = panel_vertices
        self.camber_slopes = camber_slopes
        self.wedge_angles = wedge_angles
        self.surface_id = surface_id
        self.control_surface_id = control_surface_id
        self.is_leading_edge = is_leading_edge
        self.is_trailing_edge = is_trailing_edge
        
        # If passed in from mirror_distribution or unpacking, use them directly
        if total_panels is not None:
            self.total_panels = total_panels
        else:
            self.total_panels = int(panel_vertices.shape[0])
            
        if total_strips is not None:
            self.total_strips = total_strips
        else:
            self.total_strips = int(jnp.sum(is_leading_edge))

    # --- Derived Physics (@properties) ---
    @property
    def bound_vortex_left(self):
        verts = self.panel_vertices
        return 0.75 * verts[:, 0, :] + 0.25 * verts[:, 1, :]
    
    @property
    def bound_vortex_right(self):
        verts = self.panel_vertices
        return 0.75 * verts[:, 3, :] + 0.25 * verts[:, 2, :]

    @property
    def bound_vortex_inboard(self):
        left = self.bound_vortex_left
        right = self.bound_vortex_right

        # True if Left is further outboard (larger absolute Y) than Right.
        flip = jnp.abs(left[:, 1]) > jnp.abs(right[:, 1])

        # Expand mask from (N,) to (N, 1) so it broadcasts across X, Y, Z
        return jnp.where(flip[:, None], right, left)

    @property
    def bound_vortex_outboard(self):
        left = self.bound_vortex_left
        right = self.bound_vortex_right

        flip = jnp.abs(left[:, 1]) > jnp.abs(right[:, 1])
        return jnp.where(flip[:, None], left, right)

    @property
    def bound_vortex_center(self):
        # Center is mathematically identical regardless of inboard/outboard flip
        return 0.5 * (self.bound_vortex_left + self.bound_vortex_right)

    @property
    def bound_vortex_A(self):
        """Returns the vortex endpoint with the strictly smaller Y-coordinate for VIC calculation"""
        left = self.bound_vortex_left
        right = self.bound_vortex_right

        flip = left[:, 1] > right[:, 1]
        return jnp.where(flip[:, None], right, left)

    @property
    def bound_vortex_B(self):
        """Returns the bound vortex endpoint with the strictly larger Y-coordinate for VIC calculation"""
        left = self.bound_vortex_left
        right = self.bound_vortex_right

        flip = left[:, 1] > right[:, 1]
        return jnp.where(flip[:, None], left, right)

    @property
    def collocation_points(self):
        verts = self.panel_vertices
        colloc_left = 0.25 * verts[:, 0, :] + 0.75 * verts[:, 1, :]
        colloc_right = 0.25 * verts[:, 3, :] + 0.75 * verts[:, 2, :]
        return 0.5 * (colloc_left + colloc_right)

    @property
    def normal_vectors(self):
        verts = self.panel_vertices
        diag_1 = verts[:, 2, :] - verts[:, 0, :]
        diag_2 = verts[:, 1, :] - verts[:, 3, :]

        # Swapped order: diag_2 x diag_1 forces the right-hand rule to point UP (+Z)
        raw_normals = jnp.cross(diag_2, diag_1)

        return raw_normals / jnp.linalg.norm(raw_normals, axis=1, keepdims=True)
    
    @property
    def chord_lengths(self):
        verts = self.panel_vertices
        chord_left = jnp.linalg.norm(verts[:, 1, :] - verts[:, 0, :], axis=-1)
        chord_right = jnp.linalg.norm(verts[:, 2, :] - verts[:, 3, :], axis=-1)
        return (chord_left + chord_right) / 2.0

    @property
    def incidence_angle(self):
        verts = self.panel_vertices

        mid_front = 0.5 * (verts[:, 0, :] + verts[:, 3, :])
        mid_back = 0.5 * (verts[:, 1, :] + verts[:, 2, :])

        dx = mid_back[:, 0] - mid_front[:, 0]
        dz = mid_back[:, 2] - mid_front[:, 2]

        physical_twist = jnp.arctan2(-dz, dx)
        camber_angle = jnp.arctan(self.camber_slopes)

        return physical_twist + camber_angle
    
    @property
    def panel_areas(self):
        verts = self.panel_vertices
        diag_1 = verts[:, 2, :] - verts[:, 0, :]
        diag_2 = verts[:, 1, :] - verts[:, 3, :]
        raw_normals = jnp.cross(diag_2, diag_1)
        return 0.5 * jnp.linalg.norm(raw_normals, axis=1)
    
    @property
    def strip_ids(self):
        return jnp.cumsum(self.is_leading_edge) - 1
    
    @property
    def panels_per_strip(self):
        strip_ids = self.strip_ids
        panel_ones = jnp.ones_like(strip_ids, dtype=jnp.float32)
        stripwise_panels = jax.ops.segment_sum(panel_ones, strip_ids, num_segments=self.total_strips)
        return stripwise_panels[strip_ids]
    
def mirror_distribution(vd: VortexDistribution) -> VortexDistribution:
    """ Creates the symmetric left-side counterpart of a right-side wing. """
    
    # 1. Flip the Y coordinates (Index 1)
    flipped_verts = vd.panel_vertices.at[:, :, 1].multiply(-1.0)
    
    # 2. Reorder the corners to fix the winding (Maintain UPWARD normals)
    # Original: [0: Front-Left, 1: Back-Left, 2: Back-Right, 3: Front-Right]
    # Mirrored: Swap Left and Right
    # New order: [3, 2, 1, 0] 
    mirrored_verts = flipped_verts[:, jnp.array([3, 2, 1, 0]), :]
    
    # Create the new kwargs dict
    mirrored_kwargs = {}
    for field in dataclasses.fields(vd):
        key = field.name
        if key == "panel_vertices":
            mirrored_kwargs[key] = mirrored_verts
        else:
            # Copy all other flags, surface IDs, and strip IDs as-is
            mirrored_kwargs[key] = getattr(vd, key)
            
    return VortexDistribution(**mirrored_kwargs) 

def merge_vortex_distributions(vd_list: list[VortexDistribution]) -> VortexDistribution:
    """
    Merges a list of flattened VortexDistributions into a single global unstructured mesh.
    Highly optimized for JAX by using single-pass concatenations.
    """
    if not vd_list:
        raise ValueError("Cannot merge an empty list of VortexDistributions.")
    if len(vd_list) == 1:
        return vd_list[0]

    merged_kwargs = {}
    
    # Iterate through the fields defined in the Equinox module
    for field in dataclasses.fields(vd_list[0]):
        key = field.name
        first_val = getattr(vd_list[0], key)

        if key == "strip_id":
            # Accumulate strip IDs with a running offset to guarantee global uniqueness
            adjusted_strip_ids = []
            current_offset = 0
            
            for vd in vd_list:
                val = getattr(vd, key)
                adjusted_strip_ids.append(val + current_offset)
                
                if val.size > 0:
                    current_offset += jnp.max(val) + 1
                    
            merged_kwargs[key] = jnp.concatenate(adjusted_strip_ids, axis=0)
            
        elif key in ["total_panels", "total_strips"]:
            # Explicitly sum the structural integers across all meshes
            merged_kwargs[key] = sum(getattr(vd, key) for vd in vd_list)
            
        elif isinstance(first_val, jnp.ndarray):
            # One-shot concatenation for all geometry, flags, and surface IDs
            arrays_to_concat = [getattr(vd, key) for vd in vd_list]
            merged_kwargs[key] = jnp.concatenate(arrays_to_concat, axis=0)
            
        else:
            # Fallback for static configuration fields (assumes identical across the list)
            merged_kwargs[key] = first_val

    return VortexDistribution(**merged_kwargs)

# ----------------------------------------------------------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------------------------------------------------------

def convert_to_segmented_wing(wing):
    """ Returns a tuple of (root_segment, tip_segment) for unsegmented wings. """
    
    # If it already has segments, just return them as-is
    if hasattr(wing, 'segments') and len(wing.segments) > 0:
        return wing.segments

    # 1. Build Root Segment
    root_sweeps = WingSweeps(
        quarter_chord=wing.sweeps.quarter_chord,
        leading_edge=wing.sweeps.leading_edge
    )

    root_segment = WingSegment(
        tag='root_segment',
        percent_span_location=0.0,
        twist=wing.twists.root,
        root_chord_percent=1.0,
        dihedral_outboard=wing.dihedral,
        sweeps=root_sweeps,
        thickness_to_chord=wing.thickness_to_chord,
    )
    if hasattr(wing, 'airfoil') and wing.airfoil is not None:
        root_segment = eqx.tree_at(lambda s: s.airfoil, root_segment, wing.airfoil)

    # 2. Build Tip Segment
    tip_sweeps = WingSweeps(
        quarter_chord=0.0,
        leading_edge=1e-8,
    )

    tip_segment = WingSegment(
        tag='tip_segment',
        percent_span_location=1.0,
        twist=wing.twists.tip,
        root_chord_percent=wing.taper,
        dihedral_outboard=0.0,
        sweeps=tip_sweeps,
        thickness_to_chord=wing.thickness_to_chord,
    )
    
    if hasattr(wing, 'airfoil') and wing.airfoil is not None:
        tip_segment = eqx.tree_at(lambda s: s.airfoil, tip_segment, wing.airfoil)

    return (root_segment, tip_segment)

def validate_airfoil_resolutions(wing):
    # Semi=proofing against future Airfoil subclasses by checking name instead of isinstance
    is_airfoil = lambda node: hasattr(node, '__class__') and 'Airfoil' in node.__class__.__name__

    # Get leaves with Airfoils as stopping points
    all_leaves = jax.tree_util.tree_leaves(wing, is_leaf=is_airfoil)

    # Filter out non-Airfoil leaves
    airfoils = [leaf for leaf in all_leaves if is_airfoil(leaf)]

    if airfoils:
        resolutions = [af.coordinates.shape[0] for af in airfoils]
        if len(set(resolutions)) > 1:
            raise ValueError(f"VLM discretization requires all airfoils on a wing to have the same number of points. "
                             f"On wing '{wing.tag}' found resolutions: {set(resolutions)}.")
        else:
            return resolutions[0]
    else:
        return 2  # Number of airfoil coordinates, 2 if no airfoil for flat line

def find_intervals(wing: Wing) -> tuple[jnp.ndarray, jnp.ndarray]:
    """
    Finds every unique spanwise slicing plane (from segments and control surfaces)
    and builds non-overlapping spanwise intervals.
    """
    # 1. Collect all raw span fractions where a break occurs

    segment_boundaries = [seg.percent_span_location for seg in wing.segments] + [1.0]
    cs_span_starts = [cs.span_fraction_start for cs in wing.control_surfaces]
    cs_span_ends = [cs.span_fraction_end for cs in wing.control_surfaces]

    raw_breaks = jnp.sort(jnp.array(segment_boundaries + cs_span_starts + cs_span_ends))
    
    diffs = jnp.diff(raw_breaks)
    mask = jnp.concatenate([jnp.array([True]), diffs > 1e-6])
    unique_breaks = raw_breaks[mask]

    # Find midpoints between breaks
    eta_starts = unique_breaks[:-1]
    eta_ends = unique_breaks[1:]
    midpoints = (eta_starts + eta_ends) / 2.0
    n_intervals = len(midpoints)

    strip_segment_idx = jnp.searchsorted(jnp.array(segment_boundaries), midpoints, side='right') - 1
    strip_segment_idx = jnp.clip(strip_segment_idx, 0, len(wing.segments) - 1)

    # Escape CS handling if wing has no control surfaces

    if not hasattr(wing, 'control_surfaces') or len(wing.control_surfaces) == 0:
        le_cuts = jnp.zeros(n_intervals)
        te_cuts = jnp.ones(n_intervals)
        le_ids = jnp.full(n_intervals, -1, dtype=jnp.int32)
        te_ids = jnp.full(n_intervals, -1, dtype=jnp.int32)
        return jnp.stack([eta_starts, eta_ends, le_cuts, te_cuts, le_ids, te_ids], axis=1), strip_segment_idx

    # Convert CS info to arrays
    cs_span_starts  = jnp.array(cs_span_starts)
    cs_span_ends    = jnp.array(cs_span_ends)
    cs_chord_starts = jnp.array([cs.chord_fraction_start for cs in wing.control_surfaces])
    cs_chord_ends   = jnp.array([cs.chord_fraction_end for cs in wing.control_surfaces])

    # Find which control surfaces intersect each interval
    active_mask = (midpoints[:, None] > cs_span_starts[None, :]) & (midpoints[:, None] < cs_span_ends[None, :])

    # Find leading edge and trailing edge cuts
    # (Chord starts and ends are bound to LE/TE by WingControlSurface post_init validation)
    is_le_cs = cs_chord_starts == 0.0
    is_te_cs = cs_chord_ends == 1.0
    
    le_cuts = jnp.max(jnp.where(active_mask & is_le_cs[None, :], cs_chord_ends[None, :], 0.0), axis=1, initial=1.0)
    te_cuts = jnp.min(jnp.where(active_mask & is_te_cs[None, :], cs_chord_starts[None, :], 1.0), axis=1, initial=1.0)

    # Map the cuts to particular control surfaces
    le_active = active_mask & is_le_cs[None, :]
    te_active = active_mask & is_te_cs[None, :]

    le_id = jnp.where(jnp.any(le_active, axis=1), jnp.argmax(le_active, axis=1), -1)
    te_id = jnp.where(jnp.any(te_active, axis=1), jnp.argmax(te_active, axis=1), -1)

    return jnp.stack([eta_starts, eta_ends, le_cuts, te_cuts, le_id, te_id], axis=1), strip_segment_idx

def generate_spanwise_coordinates(intervals_data: jnp.ndarray, n_sw: int, cosine_spacing: bool = False) -> jnp.ndarray:
    """
    Generates piecewise spanwise coordinates (eta) guaranteeing breaks at the interval boundaries.
    
    Args:
        intervals_data: jnp.ndarray of shape (N_intervals, 4) -> [eta_start, eta_end, le_cut, te_cut]
        n_sw: int, total number of spanwise panels requested.
        cosine_spacing: bool, whether to cluster panels at interval boundaries.
        
    Returns:
        eta_vertices: jnp.ndarray of shape (n_sw + 1,)
    """
    n_intervals = intervals_data.shape[0]
    
    # Extract the bounds directly from the new interval structure
    eta_starts = intervals_data[:, 0]
    eta_ends = intervals_data[:, 1]
    
    # Safety catch: Ensure we have at least 1 panel per interval
    n_sw = jnp.maximum(n_sw, n_intervals)
    
    # 1. Proportional Allocation (Guaranteeing exactly n_sw total panels)
    widths = eta_ends - eta_starts
    cum_fractions = jnp.cumsum(widths) / jnp.sum(widths)
    
    # Subtract n_intervals to guarantee a baseline of 1 panel per interval
    n_sw_adj = n_sw - n_intervals
    cum_panels = jnp.round(cum_fractions * n_sw_adj).astype(int)
    
    # Retrieve the exact panels per interval and add the baseline 1 back
    panels_per_interval = jnp.diff(jnp.concatenate([jnp.array([0]), cum_panels])) + 1
    
    # 2. Global-to-Local Index Mapping
    cum_panels_adj = jnp.concatenate([jnp.array([0]), jnp.cumsum(panels_per_interval)])
    
    # Create the global vertex indices (0 to n_sw)
    vertex_indices = jnp.arange(n_sw + 1)
    
    # Find which interval each vertex belongs to
    interval_idx = jnp.searchsorted(cum_panels_adj, vertex_indices, side='right') - 1
    
    # Clip to prevent out-of-bounds on the very last vertex (n_sw)
    interval_idx = jnp.clip(interval_idx, 0, n_intervals - 1)
    
    # 3. Calculate local fractions
    local_i = vertex_indices - cum_panels_adj[interval_idx]
    n_local = panels_per_interval[interval_idx]
    
    # Linear fraction inside the interval (0.0 to 1.0)
    f_linear = local_i / n_local
    
    # Apply Cosine Spacing if requested
    f_spacing = jnp.where(
        cosine_spacing, 
        0.5 * (1.0 - jnp.cos(jnp.pi * f_linear)), 
        f_linear
    )
    
    # 4. Map back to global eta coordinates
    interval_starts = eta_starts[interval_idx]
    interval_ends = eta_ends[interval_idx]
    
    eta_vertices = interval_starts + f_spacing * (interval_ends - interval_starts)

    interval_mapping = interval_idx[:-1]
    
    return eta_vertices, interval_mapping


def generate_chordwise_coordinates(le_cut: float, te_cut: float, n_cw: int, cosine_spacing: bool = False) -> jnp.ndarray:
    """
    Generates piecewise chordwise coordinates (0.0 to 1.0) for a single strip.
    """
    # Define the 3 potential chordwise sections: 
    breaks = jnp.array([0.0, le_cut, te_cut, 1.0]) # [Leading Edge -> le_cut], [le_cut -> te_cut], [te_cut -> Trailing Edge]
    widths = jnp.diff(breaks)  # Calculate physical widths of these sections
    n_cw = jnp.maximum(n_cw, 3)  # Safety catch
    
    # Proportional Allocation ()
    total_width = jnp.sum(widths)
    cum_fractions = jnp.cumsum(widths) / jnp.maximum(total_width, 1e-8)
    cum_panels = jnp.round(cum_fractions * n_cw).astype(int) # We must distribute exactly n_c panels, rounding off 0-widths intervales
    panels_per_interval = jnp.diff(jnp.concatenate([jnp.array([0]), cum_panels]))
    
    # Global-to-Local Index Mapping
    cum_panels_adj = jnp.concatenate([jnp.array([0]), jnp.cumsum(panels_per_interval)])
    vertex_indices = jnp.arange(n_cw + 1)
    
    interval_idx = jnp.searchsorted(cum_panels_adj, vertex_indices, side='right') - 1
    interval_idx = jnp.clip(interval_idx, 0, 2)
    
    # Calculate local fractions
    local_i = vertex_indices - cum_panels_adj[interval_idx]
    n_local = panels_per_interval[interval_idx]
    f_linear = jnp.where(n_local > 0, local_i / jnp.maximum(n_local, 1), 0.0)
    
    # Chordwise cosine spacing is currently present, but unsupported
    f_spacing = jnp.where(
        cosine_spacing, 
        0.5 * (1.0 - jnp.cos(jnp.pi * f_linear)), 
        f_linear
    )
    
    # Map back to global chord coordinates (0.0 to 1.0)
    interval_starts = breaks[interval_idx]
    interval_ends = breaks[interval_idx + 1]
    
    x_c_vertices = interval_starts + f_spacing * (interval_ends - interval_starts)
    
    return x_c_vertices


def calculate_macro_properties(wing, eta_vertices: jnp.ndarray, semispan: float) -> tuple:
    """
    Vectorized lofting of the structural wing, directly evaluated at the computational grid.
    """
    # 1. Extract Structural Nodes (Assuming len(segments) == N_nodes)
    seg_etas = jnp.stack([seg.percent_span_location for seg in wing.segments])
    seg_c_fracs = jnp.stack([seg.root_chord_percent for seg in wing.segments])
    seg_twists = jnp.stack([seg.twist for seg in wing.segments])
    
    # Sweeps and dihedrals dictate the interval outboard of the node
    qc_sweeps = jnp.stack([seg.sweeps.quarter_chord for seg in wing.segments])[:-1]
    dihedrals = jnp.stack([seg.dihedral_outboard for seg in wing.segments])[:-1]

    # 2. Calculate Physical Geometry at the Nodes
    seg_Y = seg_etas * semispan
    seg_c = seg_c_fracs * wing.chords.root
    
    # Deltas between nodes
    dY = jnp.diff(seg_Y)
    dc = jnp.diff(seg_c)
    
    # 3. Vectorized Sweep & Dihedral projection
    dX_qc = dY * jnp.tan(qc_sweeps)
    dX_LE = dX_qc - 0.25 * dc  # Shift reference frame to LE
    dZ_LE = dY * jnp.tan(dihedrals)
    
    # 4. Cumulative sum to get actual 3D coordinates of the structural nodes
    node_X_LE = jnp.concatenate([jnp.array([0.0]), jnp.cumsum(dX_LE)])
    node_Z_LE = jnp.concatenate([jnp.array([0.0]), jnp.cumsum(dZ_LE)])

    # Map to individual strips.
    
    strip_X_LE = jnp.interp(eta_vertices, seg_etas, node_X_LE)
    strip_Y = jnp.interp(eta_vertices, seg_etas, seg_Y)
    strip_Z_LE = jnp.interp(eta_vertices, seg_etas, node_Z_LE)
    
    strip_c = jnp.interp(eta_vertices, seg_etas, seg_c)
    strip_twist = jnp.interp(eta_vertices, seg_etas, seg_twists)

    return strip_X_LE, strip_Y, strip_Z_LE, strip_c, strip_twist


def morph_to_3d_mesh(xi_grid, strip_X_LE, strip_Y, strip_Z_LE, strip_c, strip_twist):
    """
    Morphs the non-dimensional topological grid into a 3D VLM panel mesh.
    Returns an array of shape (n_sw, n_cw, 4, 3) containing the 4 corner vertices of every panel.
    """
    # 1. Extract Left (L) and Right (R) macroscopic boundaries for each strip
    # Shapes become (n_sw, 1) so they broadcast against the (n_sw, n_cw + 1) grids
    c_L = strip_c[:-1][:, None]
    c_R = strip_c[1:][:, None]

    twist_L = strip_twist[:-1][:, None]
    twist_R = strip_twist[1:][:, None]
    
    X_LE_L = strip_X_LE[:-1][:, None]
    X_LE_R = strip_X_LE[1:][:, None]
    
    Y_L = strip_Y[:-1][:, None]
    Y_R = strip_Y[1:][:, None]
    
    Z_LE_L = strip_Z_LE[:-1][:, None]
    Z_LE_R = strip_Z_LE[1:][:, None]

    # 2. Scale up to physical 2D coordinates (still relative to the Leading Edge pivot)
    # Shapes: (n_sw, n_cw + 1)
    x_2d_L = xi_grid * c_L
    z_2d_L = jnp.zeros_like(x_2d_L)
    
    x_2d_R = xi_grid * c_R
    z_2d_R = jnp.zeros_like(x_2d_R)

    # 3. Apply Twist Rotation (Pitching around the Leading Edge pivot)
    x_rot_L =  x_2d_L * jnp.cos(twist_L) + z_2d_L * jnp.sin(twist_L)
    z_rot_L = -x_2d_L * jnp.sin(twist_L) + z_2d_L * jnp.cos(twist_L)

    x_rot_R =  x_2d_R * jnp.cos(twist_R) + z_2d_R * jnp.sin(twist_R)
    z_rot_R = -x_2d_R * jnp.sin(twist_R) + z_2d_R * jnp.cos(twist_R)

    # 4. Translate to the 3D Swept/Dihedraled Space
    # These contain the exact 3D coordinates for every chordwise vertex line 
    X_3D_L = X_LE_L + x_rot_L
    Y_3D_L = jnp.broadcast_to(Y_L, X_3D_L.shape)  # Y is constant along the chord
    Z_3D_L = Z_LE_L + z_rot_L
    
    X_3D_R = X_LE_R + x_rot_R
    Y_3D_R = jnp.broadcast_to(Y_R, X_3D_R.shape)
    Z_3D_R = Z_LE_R + z_rot_R

    # 5. Assemble the Panels
    # Stack the coordinates into (X, Y, Z) points -> Shape: (n_sw, n_cw + 1, 3)
    verts_L = jnp.stack([X_3D_L, Y_3D_L, Z_3D_L], axis=-1)
    verts_R = jnp.stack([X_3D_R, Y_3D_R, Z_3D_R], axis=-1)
    
    # Slice them to define the 4 corners of each panel (Front to Back)
    front_left  = verts_L[:, :-1, :]
    back_left   = verts_L[:, 1:, :]
    back_right  = verts_R[:, 1:, :]
    front_right = verts_R[:, :-1, :]
    
    # Stack into final panel array. 
    # Counter-clockwise ordering ensures normal vectors point UP (Right Hand Rule)
    panel_vertices = jnp.stack([front_left, back_left, back_right, front_right], axis=2)
    
    return panel_vertices

@inputs(
    "settings.analysis.aerodynamics: VLMSettings",
    "settings.analysis.aerodynamics.discretize_control_surfaces",
    "settings.analysis.aerodynamics.vortices.wing_spanwise_vortices",
    "settings.analysis.aerodynamics.vortices.wing_chordwise_vortices",
    "system.wings",
)
@outputs(
    "system.analysis_data['vortex_distribution']",
    "settings.analysis.aerodynamics.vortices.chordwise_cosine"
)
def discretize_surfaces(state: "State", system: "Aircraft", settings: "Settings"):
    
    # Pre-Processing ---------------------------------------------------------------------------------------------------

    # Unpacking 
    vlm_settings: VLMSettings = settings.analysis.aerodynamics  # type: ignore
    updated_system = system
    VD_list = []
        
    # Reformat original wings to have at least 2 segments and additional values for processing later
    for wing_idx, wing in enumerate(system.wings):  # type: ignore
        wing: Wing
        if len(wing.segments) == 0:
            # convert to preferred format for the panelization loop
            new_segments = convert_to_segmented_wing(wing)
            wing = eqx.tree_at(lambda w: w.segments, wing, new_segments)
        else:
            # TODO: Add support for All_Moving_Surface class
            for segment in wing.segments:
                if len(segment.control_surfaces) > 0:
                    raise ValueError(f"Found control surfaces on segment '{segment.tag}' of wing '{wing.tag}'. \
                                     Control surfaces must be attributes of the wing itself.")

        # Non-Dimensional Panelization ---------------------------------------------------------------------------------
        
        interval_data, strip_interval_map = find_intervals(wing)
        
        try:
            n_sw = vlm_settings.vortices.wings_n_spanwise[wing_idx]
            n_cw = vlm_settings.vortices.wings_n_chordwise[wing_idx]
        except TypeError:
            n_sw = vlm_settings.vortices.wings_n_spanwise
            n_cw = vlm_settings.vortices.wings_n_chordwise
        
        if len(interval_data) > n_sw or n_cw < 3:  # type: ignore
            warnings.warn(
                f"Specified number of wing vortices ({n_sw}, {n_cw}) "
                f"is less than the required spanwise breaks ({len(interval_data)}). "
                f"Increasing number of wing spanwise vortices to prevent mesh collapse."
            )  # Handled in generation functions below
        
        # Calculate strip eta (non-dimensional y-coordinate) (Shape: (n_sw +1,))
        eta, strip_interval_map = generate_spanwise_coordinates(
            interval_data, n_sw, 
            vlm_settings.vortices.spanwise_cosine)

        # Calculate strip xi (non-dimensional x-coordinate) (Shape: (n_sw, n_cw + 1))
        strip_le_cuts = interval_data[:, 2][strip_interval_map]
        strip_te_cuts = interval_data[:, 3][strip_interval_map]

        vmap_chordwise = jax.vmap(generate_chordwise_coordinates, in_axes=(0, 0, None, None))
        xi_grid = vmap_chordwise(
            strip_le_cuts, strip_te_cuts, n_cw,
            False) # Force linear chordwise spacing for Pistolesi's theorem (assumed in coefficient integration)

        # Map panels to control surfaces
        xi_mid = (xi_grid[:, :-1] + xi_grid[:, 1:]) / 2.0
        strip_le_ids = interval_data[:, 4][strip_interval_map]
        strip_te_ids = interval_data[:, 5][strip_interval_map]
        
        panel_cs_id = jnp.full_like(xi_mid, -1, dtype=jnp.int32) # Default to -1 to indicate panel belongs to wing itself
        panel_cs_id = jnp.where(
            xi_mid < strip_le_cuts[:, None],
            strip_le_ids[:, None],
            panel_cs_id) # If xi < LE cut, assign local LE CS ID
        panel_cs_id = jnp.where(
            xi_mid > strip_te_cuts[:, None],
            strip_te_ids[:, None],
            panel_cs_id)  # If xi > TE cut, assign local TE CS ID
        
        # Geometric Corrections ----------------------------------------------------------------------------------------

        # Calculate strip zeta (non-dimensional z-coordinate) (Shape: (n_sw, n_cw + 1))
        n_af_pts = validate_airfoil_resolutions(wing)
        flat_x = jnp.linspace(0.0, 1.0, n_af_pts // 2)
        flat_z = jnp.zeros(n_af_pts // 2)

        seg_camber_x = jnp.stack([
            seg.airfoil.x_lower_surface if getattr(seg, 'airfoil', None) else flat_x 
            for seg in wing.segments
        ]) # type: ignore

        seg_camber_z = jnp.stack([
            seg.airfoil.camber if getattr(seg, 'airfoil', None) else flat_z 
            for seg in wing.segments
        ])  # type: ignore

        seg_wedge_angle = jnp.stack([
            seg.airfoil.wedge_angle if getattr(seg, 'airfoil', None) else 0.0
            for seg in wing.segments
        ])  # type: ignore

        strip_camber_x      = seg_camber_x[strip_interval_map]
        strip_camber_z      = seg_camber_z[strip_interval_map]
        strip_wedge_angle   = seg_wedge_angle[strip_interval_map]

        xi_colloc = 0.25 * xi_grid[:, :-1] + 0.75 * xi_grid[:, 1:]

        vmap_interp = jax.vmap(jnp.interp, in_axes=(0, 0, 0))

        # Finite difference local camber slope/incidence angle
        zeta_fwd = vmap_interp(xi_colloc + 1e-4, strip_camber_x, strip_camber_z)
        zeta_bwd = vmap_interp(xi_colloc - 1e-4, strip_camber_x, strip_camber_z)

        camber_slopes = (zeta_fwd - zeta_bwd) / 2e-4

        # Calculate strip macro-level properties
        semispan = wing.spans.projected / 2.0 if wing.symmetric else wing.spans.projected 
        strip_X_LE, strip_Y, strip_Z_LE, strip_c, strip_twist = calculate_macro_properties(wing, eta, semispan)

        morph_results = morph_to_3d_mesh(xi_grid, strip_X_LE, strip_Y, strip_Z_LE, strip_c, strip_twist)
        
        if wing.vertical:
            y_coords = morph_results[:, :, :, 1]
            z_coords = morph_results[:, :, :, 2]
            
            morph_results = morph_results.at[:, :, :, 1].set(z_coords)
            morph_results = morph_results.at[:, :, :, 2].set(y_coords)


        # Flatten and pack into VortexDistribution ---------------------------------------------------------------------
        flat_vertices = (morph_results + wing.origin).reshape(-1, 4, 3)
        
        VD = VortexDistribution(
            panel_vertices=flat_vertices,
            camber_slopes=camber_slopes.reshape(-1),
            wedge_angles=strip_wedge_angle.reshape(-1),
            surface_id=jnp.full(flat_vertices.shape[0], wing_idx, dtype=jnp.int32),
            control_surface_id=panel_cs_id.reshape(-1),
            is_leading_edge=jnp.zeros_like(xi_mid, dtype=bool).at[:, 0].set(True).reshape(-1),
            is_trailing_edge=jnp.zeros_like(xi_mid, dtype=bool).at[:, -1].set(True).reshape(-1),
        )

        VD_list.append(VD)

        if wing.symmetric:

            VD_list.append(mirror_distribution(VD))
           
    full_VD = merge_vortex_distributions(VD_list)    

    updated_analysis_data = system.analysis_data | {"vortex_distribution": full_VD}
        
    updated_system  = eqx.tree_at(lambda s: s.analysis_data, updated_system, updated_analysis_data)

    updated_settings = eqx.tree_at(lambda s: s.analysis.aerodynamics, settings, vlm_settings)

    return state, updated_system, updated_settings