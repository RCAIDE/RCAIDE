# RCAIDE/Framework/Components/Wing.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Sep, 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT 
# ----------------------------------------------------------------------------------------------------------------------

import jax.numpy as jnp
import equinox as eqx

from RCAIDE.Library import Component, ComponentDimensions, ComponentAreas
from RCAIDE.Library.Components.Airfoils import Airfoil


# ----------------------------------------------------------------------------------------------------------------------
# Wing
# ----------------------------------------------------------------------------------------------------------------------


class WingDimensions(ComponentDimensions):

    root: float = 0.0
    tip:  float = 0.0


class WingSweeps(WingDimensions):
    leading_edge:   float = 0.0
    quarter_chord:  float = 0.0
    half_chord:     float = 0.0


class WingChords(WingDimensions):
    mean_aerodynamic:   float = 0.0
    mean_geometric:     float = 0.0


class WingSegment(Component):

    tag: str = eqx.field(static=True, default='Wing Segment')
    airfoil: Airfoil | None = None
    control_surfaces: tuple = eqx.field(default_factory=tuple)

    # Specialty Attributes

    thickness_to_chord: float = 0.0
    root_chord_percent: float = 0.0
    percent_span_location: float = 0.0
    twist: float = 0.0
    dihedral_outboard: float = 0.0

    sweeps: WingSweeps = eqx.field(default_factory=WingSweeps)
    chords: WingChords = eqx.field(default_factory=WingChords)

    @property
    def taper(self):
        
        # Sidestep Equinox LeafWrappers
        if hasattr(self.chords.root, "value"): safe_root = jnp.maximum(self.chords.root.value, 1e-8) # type: ignore
        else: safe_root = jnp.maximum(self.chords.root, 1e-8)

        if hasattr(self.chords.tip, "value"): safe_tip = self.chords.tip.value
        else: safe_tip = self.chords.tip
        
        return safe_tip / safe_root


class WingControlSurface(Component):

    tag: str = eqx.field(static=True, default='Wing Control Surface')

    span_fraction_start: float  = 0.0
    span_fraction_end: float    = 0.0

    chord_fraction_start: float = 0.0
    chord_fraction_end: float   = 1.0

    hinge_fraction: float       = 0.0
    root_chord_percent: float   = 0.0

    sign_duplicate: float       = 1.0
    deflection: float           = 0.0
    configuration_type: str     = eqx.field(static=True, default='single_slotted')

    gain: float                 = 1.0  # deflection multiplier used only for AVL

    def __post_init__(self):
        if not (self.chord_fraction_start == 0.0 or self.chord_fraction_end == 1.0):
            raise ValueError("Control surface chord fractions must terminate at either 0.0 or 1.0. "
                             "Got: ({}, {})".format(self.chord_fraction_start, self.chord_fraction_end))


class Wing(Component):

    tag:                str             = eqx.field(static=True, default='Wing')
    airfoil:            Airfoil | None  = None
    control_surfaces:   Component       = eqx.field(default_factory=lambda: Component(tag='Control Surfaces'))

    # Specialty Attributes

    symmetric: bool     = eqx.field(static=True, default=True)
    vertical: bool      = eqx.field(static=True, default=False)
    t_tail: bool        = eqx.field(static=True, default=False)
    high_lift: bool     = eqx.field(static=True, default=False)
    symbolic: bool      = eqx.field(static=True, default=False)
    high_mach: bool     = eqx.field(static=True, default=False)
    vortex_lift: bool   = eqx.field(static=True, default=False)

    taper:                      float   = 0.0
    dihedral:                   float   = 0.0
    aspect_ratio:               float   = 0.0
    thickness_to_chord:         float   = 0.0
    exposed_root_chord_offset:  float   = 0.0

    single_side_aerodynamic_center: jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty((0, 3)))

    transition_x_upper: float = 0.0
    transition_x_lower: float = 0.0

    dynamic_pressure_ratio: float = 0.0

    aerodynamic_center: jnp.ndarray = eqx.field(default_factory=lambda: jnp.empty((0, 3)))

    spans:  WingDimensions  = eqx.field(default_factory=lambda: WingDimensions(ordinal_direction=True))
    twists: WingDimensions  = eqx.field(default_factory=WingDimensions)
    chords: WingChords      = eqx.field(default_factory=WingDimensions)
    sweeps: WingSweeps      = eqx.field(default_factory=WingSweeps)

    def __post_init__(self):
        new_taper, new_chords = self.validate_chords()
        object.__setattr__(self, "taper", new_taper)
        object.__setattr__(self, "chords", new_chords)

        updated_segments = []

        for idx, seg in enumerate(self.segments):
            root = new_chords.root * seg.root_chord_percent
            if idx == len(self.segments) -1:
                tip = new_chords.tip
            else:
                tip = new_chords.root * self.segments[idx + 1].root_chord_percent
            
            new_seg = eqx.tree_at(lambda s: s.chords, seg, WingChords(root=root, tip=tip))
            updated_segments.append(new_seg)
        
        object.__setattr__(self, "segments", updated_segments)
    
    def validate_chords(self) -> tuple:
        
        root = self.chords.root
        tip = self.chords.tip
        taper = self.taper

        new_taper = taper
        new_chords = self.chords
        
        # Count how many variables the user explicitly set
        # (Assuming 0.0 is the default "unset" value in your legacy code)
        provided = sum([root != 0.0, tip != 0.0, taper != 0.0])
        
        if provided < 2:
            raise ValueError(
                f"Wing geometry under-defined. You must provide at least two of "
                f"(root, tip, taper). Currently provided: root={root}, tip={tip}, taper={taper}"
            )

        elif provided == 2:
            # Auto-complete the missing variable
            
            if tip == 0.0:
                # Update the nested frozen child module cleanly
                new_chords = eqx.tree_at(lambda c: c.tip, new_chords, root * taper)
            elif taper == 0.0:
                new_taper = tip / root
            elif root == 0.0:
                new_chords = eqx.tree_at(lambda c:c.root, new_chords, tip / taper)
                
            return new_taper, new_chords
                
        elif provided == 3:
            # All three provided: Validate mathematical consistency
            if abs(tip - (root * taper)) > 1e-2:
                raise ValueError(
                    f"Incompatible geometry for wing '{self.tag}': The provided tip chord ({tip}) "
                    f"does not match root * taper ({root * taper})."
                )
            
        return new_taper, new_chords

    @staticmethod
    def _compute_segment_properties(
        seg_span_fractions: jnp.ndarray,       # Shape: (N+1,)
        seg_root_chord_fractions: jnp.ndarray, # Shape: (N+1,)
        wing_root_chord: float,
        wing_projected_span: float,
        is_symmetric: float,
        wing_exposed_root_offset: float,
        wing_t_c: float,
        seg_t_c: jnp.ndarray                   # Shape: (N,)
    ) -> tuple[
        jnp.ndarray, jnp.ndarray, jnp.ndarray, jnp.ndarray, 
        jnp.ndarray, jnp.ndarray, jnp.ndarray, jnp.ndarray
    ]:
        """Computes basic geometries for each individual segment."""
        symm_mult = 1.0 if is_symmetric else 0.0
        wing_semispan = wing_projected_span / (1.0 + symm_mult)
        
        seg_span_fractions_diff = seg_span_fractions[1:] - seg_span_fractions[:-1]
        seg_dy = seg_span_fractions_diff * wing_semispan
        
        # Calculate chords in absolute dimensions
        seg_c_root = wing_root_chord * seg_root_chord_fractions[:-1]
        seg_c_tip = wing_root_chord * seg_root_chord_fractions[1:]
        
        # Apply exposed root offset to the very first segment (if applicable)
        # Using jnp.where avoids mutating arrays directly, which is safer in JAX
        if wing_exposed_root_offset > 0.0:
            offset_val = wing_exposed_root_offset * ((seg_c_tip[0] - seg_c_root[0]) / seg_dy[0])
            seg_c_root = seg_c_root.at[0].add(offset_val)
            
        seg_tapers = seg_c_tip / seg_c_root
        
        # Segment Mean Aerodynamic Chord
        seg_macs = seg_c_root * (2.0 / 3.0) * ((1.0 + seg_tapers + seg_tapers**2) / (1.0 + seg_tapers))
        
        # Segment Areas
        seg_s_ref = seg_dy * (seg_c_root + seg_c_tip) * 0.5
        seg_s_exposed = seg_s_ref * 1.0
        
        if wing_exposed_root_offset > 0.0:
            exposed_area_0 = (seg_dy[0] - wing_exposed_root_offset) * (seg_c_root[0] + seg_c_tip[0]) * 0.5
            seg_s_exposed = seg_s_exposed.at[0].set(exposed_area_0)
            
        if is_symmetric:
            seg_s_ref = seg_s_ref * 2.0
            seg_s_exposed = seg_s_exposed * 2.0
            
        # Segment Wetted Area
        seg_s_wet = jnp.where(
            wing_t_c < 0.05, 
            2.003 * seg_s_exposed, 
            (1.977 + 0.52 * seg_t_c) * seg_s_exposed
        )
        
        return seg_dy, seg_c_root, seg_c_tip, seg_tapers, seg_macs, seg_s_ref, seg_s_exposed, seg_s_wet

    @staticmethod
    def _compute_global_planform(
        seg_dy: jnp.ndarray,                   # Shape: (N,)
        seg_c_root: jnp.ndarray,               # Shape: (N,)
        seg_c_tip: jnp.ndarray,                # Shape: (N,)
        seg_s_ref: jnp.ndarray,                # Shape: (N,)
        seg_s_wet: jnp.ndarray,                # Shape: (N,)
        seg_span_fractions: jnp.ndarray,       # Shape: (N+1,)
        seg_quarter_chord_sweeps: jnp.ndarray, # Shape: (N,)
        seg_dihedrals: jnp.ndarray,            # Shape: (N+1,)
        wing_projected_span: float,
        is_symmetric: bool
    ) -> tuple[
        float, float, float, float, float, float, 
        jnp.ndarray, float, float, jnp.ndarray, jnp.ndarray, float
    ]:
        """Rolls up segment properties into global wing metrics."""
        symm_mult = 1.0 if is_symmetric else 0.0
        wing_semispan = wing_projected_span / (1.0 + symm_mult)
        
        wing_s_ref = jnp.sum(seg_s_ref)
        wing_s_wet = jnp.sum(seg_s_wet)
        wing_aspect_ratio = (wing_projected_span**2) / wing_s_ref
        
        # Total physical length and Mean Geometric Chord
        seg_lens = seg_dy / jnp.cos(seg_dihedrals[:-1])
        wing_total_span = jnp.sum(seg_lens) * (1.0 + symm_mult)
        wing_mgc = wing_s_ref / wing_projected_span
        
        # Global MAC (Analytical integral approach)
        seg_span_fractions_diff = seg_span_fractions[1:] - seg_span_fractions[:-1]
        
        B = (seg_c_root - seg_c_tip) / (-seg_span_fractions_diff + 1e-6)
        C = seg_span_fractions[:-1]
        
        integral_term_1 = (seg_c_root + B * (seg_span_fractions[1:] - C))**3
        integral_term_2 = (seg_c_root + B * (seg_span_fractions[:-1] - C))**3
        integral = (integral_term_1 - integral_term_2) / (3.0 * B + 1e-6)
        
        # Fallback for rectangular segments where B is 0 (NaN prevention)
        rec_mac = (seg_c_root**2) * seg_span_fractions_diff
        integral = jnp.where(jnp.isnan(integral), rec_mac, integral)
        integral = jnp.where(integral == 0., rec_mac, integral)
        wing_mac = (wing_semispan * (1.0 + symm_mult) / wing_s_ref) * jnp.sum(integral)
        
        # Sweeps
        r_offsets = seg_c_root / 4.0
        t_offsets = seg_c_tip / 4.0
        seg_le_sweeps = jnp.arctan((r_offsets + jnp.tan(seg_quarter_chord_sweeps) * seg_dy - t_offsets) / (seg_dy + 1e-6))
        
        wing_c4_sweep = jnp.arctan(jnp.sum(seg_span_fractions_diff * jnp.tan(seg_quarter_chord_sweeps)))
        wing_le_sweep = jnp.arctan(jnp.sum(seg_span_fractions_diff * jnp.tan(seg_le_sweeps)))
        
        # AC Centroids
        dxs = jnp.cumsum(jnp.concatenate([jnp.array([0.0]), jnp.tan(seg_le_sweeps) * seg_dy]))
        dys = jnp.cumsum(jnp.concatenate([jnp.array([0.0]), seg_dy]))
        dzs = jnp.cumsum(jnp.concatenate([jnp.array([0.0]), jnp.tan(seg_dihedrals[:-1]) * seg_dy]))
        
        # Vectorized Centroid Calculation
        c = jnp.tan(seg_le_sweeps) * seg_dy
        cx = (2 * seg_c_tip * c + seg_c_tip**2 + c * seg_c_root + seg_c_tip * seg_c_root + seg_c_root**2) / (3 * (seg_c_tip + seg_c_root))
        tapers = seg_c_tip / seg_c_root
        cy = seg_dy / 3.0 * ((1.0 + 2.0 * tapers) / (1.0 + tapers))
        cz = cy * jnp.tan(seg_dihedrals[:-1])
        
        cxys = jnp.stack([cx + dxs[:-1], cy + dys[:-1], cz + dzs[:-1]], axis=0)
        wing_ac = jnp.dot(cxys, seg_s_ref / (1.0 + symm_mult)) / (wing_s_ref / (1.0 + symm_mult))
        
        wing_ss_ac = wing_ac.at[0].set(wing_ac[0] - wing_mac * 0.25)
        wing_ac = wing_ac.at[0].set(wing_ss_ac[0])
        
        if is_symmetric:
            wing_ac = wing_ac.at[1].set(0.0)

        wing_total_length = jnp.tan(wing_le_sweep) * wing_semispan + seg_c_tip[-1]
        
        return (
            wing_s_ref, wing_s_wet, wing_aspect_ratio, wing_total_span, 
            wing_mgc, wing_mac, seg_le_sweeps, wing_c4_sweep, 
            wing_le_sweep, wing_ac, wing_ss_ac, wing_total_length
        ) # type: ignore
    
    def update_geometry(self, calculate_reference_area=False, calculate_wetted_area=False):
        """Returns a new Wing instance with all geometric properties calculated and populated."""
        
        # 1. Extract Arrays, add ghost tip segment
        span_locs = jnp.array([seg.percent_span_location for seg in self.segments] + [1.0])
        root_chords_pct = jnp.array([seg.root_chord_percent for seg in self.segments] + [self.taper])
        sweeps = jnp.array([seg.sweeps.quarter_chord for seg in self.segments])
        dihedrals = jnp.array([seg.dihedral_outboard for seg in self.segments] + [0.0])
        t_cs = jnp.array([seg.thickness_to_chord for seg in self.segments])
        
        symm = float(self.symmetric)
        
        # 2. Compute Segment Geometries
        dy, c_root, c_tip, tapers, macs, s_ref_seg, s_exposed_seg, s_wet_seg = self._compute_segment_properties(
            span_locs, root_chords_pct, self.chords.root, self.spans.projected, 
            symm, self.exposed_root_chord_offset, self.thickness_to_chord, t_cs
        )
        
        # 3. Compute Global Geometries
        (total_s_ref, total_s_wet, ar, total_span, mgc, global_mac, le_sweeps, c_4_sweep, 
         le_sweep_total, ac, ss_ac, total_length) = self._compute_global_planform(
            dy, c_root, c_tip, s_ref_seg, s_wet_seg, span_locs, sweeps, dihedrals, 
            self.spans.projected, symm,
        )

        total_s_ref = jnp.where(calculate_reference_area, total_s_ref, self.areas.reference)
        total_s_wet = jnp.where(calculate_wetted_area, total_s_wet, self.areas.wetted)

        
        # 4. Create updated segments (Pure functional update)
        updated_segments = []
        for i in range(len(self.segments) - 1):
            seg = self.segments[i]
            # Assuming you have an immutable dataclass or tree update method here
            new_seg = eqx.tree_at(
                lambda s: (s.chords.mean_aerodynamic, s.areas.reference, s.areas.exposed, s.areas.wetted),
                seg,
                (macs[i], s_ref_seg[i], s_exposed_seg[i], s_wet_seg[i])
            )
            updated_segments.append(new_seg)
        updated_segments.append(self.segments[-1]) # Append the tip node unaltered
        
        # 5. Create and return the updated wing
        return eqx.tree_at(
            lambda w: (
                w.segments, w.areas.reference, w.areas.wetted, w.aspect_ratio,
                w.spans.total, w.chords.mean_geometric, w.chords.mean_aerodynamic, w.chords.tip,
                w.taper, w.sweeps.quarter_chord, w.sweeps.leading_edge, 
                w.aerodynamic_center, w.single_side_aerodynamic_center, w.lengths.total
            ),
            self,
            (
                updated_segments, total_s_ref, total_s_wet, ar,
                total_span, mgc, global_mac, c_tip[-1],
                tapers[-1] * (c_root[-1] / c_root[0]), c_4_sweep, le_sweep_total, 
                ac, ss_ac, total_length
            )
        )

    def add_subcomponent(self, subcomponent: Component, update_geometry=True):

        if isinstance(subcomponent, WingSegment):
            new_segments = self.segments + (subcomponent,)
            new_wing = eqx.tree_at(lambda s: s.segments, self, new_segments)
            if self.update_geometry:
                new_wing = new_wing.update_geometry()
            return new_wing
        
        elif isinstance(subcomponent, WingControlSurface):
            new_controls = self.control_surfaces.add_subcomponent(subcomponent)
            return eqx.tree_at(lambda s: s.control_surfaces, self, new_controls)
            

        return super().add_subcomponent(subcomponent)
