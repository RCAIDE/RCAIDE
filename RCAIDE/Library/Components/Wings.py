# RCAIDE/Framework/Components/Wing.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Sep, 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT 
# ----------------------------------------------------------------------------------------------------------------------

import RNUMPY as rp

import chex
from dataclasses import field

import RCAIDE.Library as rcl
from RCAIDE.Library.Component import ComponentType


# ----------------------------------------------------------------------------------------------------------------------
# Wing
# ----------------------------------------------------------------------------------------------------------------------


@chex.dataclass(kw_only=True)
class WingDimensions(rcl.ComponentDimensions):

    root: float = 0.0
    tip: float = 0.0


@chex.dataclass(kw_only=True)
class WingSegment(rcl.Component):

    tag: str = 'Wing Segment'
    airfoil: rcl.Component = None

    # Specialty Attributes

    thickness_to_chord: float = 0.0
    percent_span_location: float = 0.0
    twist: float = 0.0
    dihedral_outboard: float = 0.0

    sweeps: rcl.ComponentDimensions = field(default_factory=lambda: rcl.ComponentDimensions())

    def __post_init__(self):
        self.sweeps.leading_edge = None
        self.sweeps.quarter_chord = 0.0
        self.sweeps.half_chord = 0.0


@chex.dataclass(kw_only=True)
class WingControlSurface(rcl.Component):

    tag: str = 'Wing Control Surface'

    span: float                 = 0.0
    span_fraction_start: float  = 0.0
    span_fraction_end: float    = 0.0

    hinge_fraction: float       = 0.0
    chord_fraction: float       = 0.0

    sign_duplicate: float       = 1.0
    deflection: float           = 0.0
    configuration_type: str     = 'single_slotted'

    gain: float                 = 1.0  # deflection multiplier used only for AVL


@chex.dataclass(kw_only=True)
class Wing(rcl.Component):

    tag:                str             = 'Wing'
    airfoil:            rcl.Component   = None
    control_surfaces:   rcl.Component   = field(default_factory=lambda: rcl.Component(tag='Control Surfaces'))

    # Specialty Attributes

    symmetric: bool     = True
    vertical: bool      = False
    t_tail: bool        = False
    high_lift: bool     = False
    symbolic: bool      = False
    high_mach: bool     = False
    vortex_lift: bool   = False

    taper:                      float   = 0.0
    dihedral:                   float   = 0.0
    aspect_ratio:               float   = 0.0
    thickness_to_chord:         float   = 0.0
    exposed_root_chord_offset:  float   = 0.0

    single_side_aerodynamic_center: rp.ndarray = None

    transition_x_upper: float = 0.0
    transition_x_lower: float = 0.0

    dynamic_pressure_ratio: float = 0.0

    aerodynamic_center: rp.ndarray = field(default_factory=lambda: rp.zeros(3))

    spans:  WingDimensions = field(default_factory=WingDimensions)
    chords: WingDimensions = field(default_factory=WingDimensions)
    twists: WingDimensions = field(default_factory=WingDimensions)
    sweeps: WingDimensions = field(default_factory=WingDimensions)

    def __post_init__(self):

        self.spans.ordinal_direction = True

        self.chords.mean_aerodynamic = 0.0
        self.chords.mean_geometric = 0.0

        self.sweeps.leading_edge = None
        self.sweeps.quarter_chord = 0.0
        self.sweeps.half_chord = 0.0

    def _update_segment_properties(self, update_areas=False):

        exposed_root_chord_offset = self.exposed_root_chord_offset
        symm                      = self.symmetric
        semispan                  = self.spans.projected*0.5 * (2 - symm)
        t_c_w                     = self.thickness_to_chord
        num_segments              = len(self.segments)

        total_wetted_area            = 0.
        total_reference_area         = 0.
        root_chord                   = self.chords.root

        for i_segs in range(num_segments):
            if i_segs == num_segments-1:
                continue
            else:
                span_seg  = semispan*(self.segments[i_segs+1].percent_span_location
                                      - self.segments[i_segs].percent_span_location)
                segment   = self.segments[i_segs]

                chord_root    = root_chord * self.segments[i_segs].root_chord_percent
                chord_tip     = root_chord * self.segments[i_segs+1].root_chord_percent

                if i_segs == 0:
                    chord_root     = chord_root + exposed_root_chord_offset*((chord_tip - chord_root)/span_seg)

                taper         = chord_tip/chord_root
                mac_seg       = chord_root  * 2/3 * ((1 + taper  + taper**2)/(1 + taper))
                Sref_seg      = span_seg*(chord_root+chord_tip)*0.5
                S_exposed_seg = Sref_seg

                if i_segs == 0:
                    S_exposed_seg = (span_seg-exposed_root_chord_offset)*(chord_root+chord_tip)*0.5

                if self.symmetric:
                    Sref_seg = Sref_seg * 2
                    S_exposed_seg = S_exposed_seg * 2

                # compute wetted area of segment
                if t_c_w < 0.05:
                    Swet_seg = 2.003 * S_exposed_seg
                else:
                    Swet_seg = (1.977 + 0.52 * t_c_w) * S_exposed_seg

                segment.taper                   = taper

                segment.chords                  = WingDimensions()
                segment.chords.mean_aerodynamic = mac_seg

                segment.areas                   = rcl.ComponentAreas()
                segment.areas.reference         = Sref_seg
                segment.areas.exposed           = S_exposed_seg
                segment.areas.wetted            = Swet_seg

                total_wetted_area    = total_wetted_area + Swet_seg
                total_reference_area = total_reference_area + Sref_seg

        if self.areas.reference == 0. or update_areas:
            self.areas.reference = total_reference_area

        if self.areas.wetted == 0. or update_areas:
            self.areas.wetted    = total_wetted_area


    def make_segmented_planform(self):

        def _segment_centroid(le_sweep,
                              seg_span,
                              dx, dy, dz,
                              taper,
                              dihedral,
                              root_chord,
                              tip_chord):

            a = tip_chord
            b = root_chord
            c = rp.tan(le_sweep)*seg_span
            cx = (2*a*c + a**2 + c*b + a*b + b**2) / (3*(a+b))
            cy = seg_span / 3. * ((1. + 2. * taper) / (1. + taper))
            cz = cy * rp.tan(dihedral)

            return rp.array([cx+dx, cy+dy, cz+dz])

        span = self.spans.projected
        RC   = self.chords.root
        sym  = self.symmetric

        # Pull all the segment data into array format
        span_locs = []
        twists    = []
        sweeps    = []
        dihedrals = []
        chords    = []
        t_cs      = []

        for seg in self.segments:

            span_locs.append(seg.percent_span_location)
            twists.append(seg.twist)
            chords.append(seg.root_chord_percent)
            sweeps.append(seg.sweeps.quarter_chord)
            t_cs.append(seg.thickness_to_chord)
            dihedrals.append(seg.dihedral_outboard)

        # Convert to arrays
        chords    = rp.array(chords)
        span_locs = rp.array(span_locs)
        sweeps    = rp.array(sweeps)
        t_cs      = rp.array(t_cs)

        # Basic calcs:
        semispan     = span/(1+sym)
        lengths_ndim = span_locs[1:]-span_locs[:-1]
        lengths_dim  = lengths_ndim*semispan
        chords_dim   = RC*chords
        tapers       = chords[1:]/chords[:-1]

        # Calculate the areas of each segment
        As = (lengths_dim*chords_dim[:-1]-(chords_dim[:-1]-chords_dim[1:])*(lengths_dim/2))

        # Calculate the weighted area, this should not include any unexposed area
        A_wets = 2*(1+0.2*t_cs[:-1])*As
        wet_area = rp.sum(A_wets)

        # Calculate the wing area
        ref_area = rp.sum(As)*(1+sym)

        # Calculate the Aspect Ratio
        AR = (span**2)/ref_area

        # Calculate the total span
        lens = lengths_dim/rp.cos(rp.array(dihedrals[:-1]))
        total_len = rp.sum(rp.array(lens))*(1+sym)

        # Calculate the mean geometric chord
        mgc = ref_area/span

        # Calculate the mean aerodynamic chord
        A = chords_dim[:-1]
        B = (A-chords_dim[1:])/(-lengths_ndim)
        C = span_locs[:-1]
        integral = ((A+B*(span_locs[1:]-C))**3-(A+B*(span_locs[:-1]-C))**3)/(3*B)
        # For the cases when the wing doesn't taper in a spot
        mask = rp.isnan(integral)
        integral = rp.where(mask, A**2 * lengths_ndim, integral)
        MAC = (semispan*(1+sym)/ref_area)*rp.sum(integral)

        # Calculate the taper ratio
        lamda = chords[-1]/chords[0]

        # the tip chord
        ct = chords_dim[-1]

        # Calculate an average t/c weighted by area
        t_c = rp.sum(As*t_cs[:-1])/(ref_area/2)

        # Calculate the segment leading edge sweeps
        r_offsets = chords_dim[:-1]/4
        t_offsets = chords_dim[1:]/4
        le_sweeps = rp.arctan((r_offsets+rp.tan(sweeps[:-1])*(lengths_dim)-t_offsets)/(lengths_dim))

        # Calculate the effective sweeps
        c_4_sweep   = rp.arctan(rp.sum(lengths_ndim*rp.tan(sweeps[:-1])))
        le_sweep_total= rp.arctan(rp.sum(lengths_ndim*rp.tan(le_sweeps)))

        # Calculate the aerodynamic center, but first the centroid
        dxs = rp.cumsum(rp.concatenate([rp.array([0]),rp.tan(le_sweeps[:-1])*lengths_dim[:-1]]))
        dys = rp.cumsum(rp.concatenate([rp.array([0]),lengths_dim[:-1]]))
        dzs = rp.cumsum(rp.concatenate([rp.array([0]),rp.tan(rp.array(dihedrals[:-2]))*lengths_dim[:-1]]))

        Cxys = []
        for i in range(len(lengths_dim)):
            Cxys.append(_segment_centroid(le_sweeps[i],
                                          lengths_dim[i],
                                          dxs[i], dys[i], dzs[i],
                                          tapers[i],
                                          dihedrals[i],
                                          chords_dim[i],
                                          chords_dim[i+1]))

        aerodynamic_center = (rp.dot(rp.transpose(rp.array(Cxys)),As)/(ref_area/(1+sym)))

        single_side_aerodynamic_center = 1*rp.array(aerodynamic_center)
        single_side_aerodynamic_center = single_side_aerodynamic_center.at[0].set(single_side_aerodynamic_center[0] - MAC*.25)

        if sym== True:
            aerodynamic_center = aerodynamic_center.at[1].set(0)

        aerodynamic_center = aerodynamic_center.at[0].set(single_side_aerodynamic_center[0])

        # Total length for supersonics
        total_length = rp.tan(le_sweep_total)*semispan + chords[-1]*RC

        # Pack stuff

        self.areas.reference         = ref_area
        self.areas.wetted            = wet_area
        self.aspect_ratio            = AR

        self.spans.total                    = total_len
        self.chords.mean_geometric          = mgc
        self.chords.mean_aerodynamic        = MAC
        self.chords.tip                     = ct
        self.taper                          = lamda
        self.sweeps.quarter_chord           = c_4_sweep
        self.sweeps.leading_edge            = le_sweep_total
        self.thickness_to_chord             = t_c
        self.aerodynamic_center             = aerodynamic_center
        self.single_side_aerodynamic_center = single_side_aerodynamic_center
        self.lengths.total                  = total_length

        # update remainder segment properties
        self._update_segment_properties()

        def add_subcomponent(self,
                         subcomponent: ComponentType,
                         sum_mass=False,
                         sum_center_of_gravity=False,
                         sum_moments_of_inertia=False
                         ):

            if isinstance(subcomponent, WingSegment):
                self.segments.append(subcomponent)
            elif isinstance(subcomponent, WingControlSurface):
                setattr(self.control_surfaces, subcomponent.get_field_name(), subcomponent)

            super().add_subcomponent(subcomponent, sum_mass, sum_center_of_gravity, sum_moments_of_inertia)









