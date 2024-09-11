# RCAIDE/Framework/Components/Wing.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Sep, 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# IMPORT 
# ----------------------------------------------------------------------------------------------------------------------

import numpy as np

from dataclasses import dataclass, field, make_dataclass

import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
# Wing
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class Wing(rcf.System):

    name: str = 'Wing'
    airfoil: rcf.Components.Airfoil = field(default_factory=lambda: rcf.Components.Airfoil.NACA_4_Series(2412))

    # Specialty Attributes

    symmetric: bool = True
    vertical: bool = False
    t_tail: bool = False
    high_lift: bool = False
    symbolic: bool = False
    high_mach: bool = False
    vortex_lift: bool = False

    taper: float = 0.0
    dihedral: float = 0.0
    aspect_ratio: float = 0.0
    thickness_to_chord: float = 0.0
    exposed_root_chord_offset: float = 0.0

    transition_x_upper: float = 0.0
    transition_x_lower: float = 0.0

    dynamic_pressure_ratio: float = 0.0

    aerodynamic_center: np.ndarray = field(default_factory=lambda: np.array([0.0, 0.0, 0.0]))

    spans   = rcf.ComponentDimensions()
    chords  = rcf.ComponentDimensions()
    twists  = rcf.ComponentDimensions()
    sweeps  = rcf.ComponentDimensions()


    def __post_init__(self):

        self.chords.mean_aerodynamic = 0.0
        self.chords.mean_geometric = 0.0
        self.chords.root = 0.0
        self.chords.tip = 0.0

        self.twists.root = 0.0
        self.twists.tip = 0.0

        self.sweeps.leading_edge = None
        self.sweeps.quarter_chord = 0.0
        self.sweeps.half_chord = 0.0


@dataclass(kw_only=True)
class WingSegment(rcf.Component):

    name: str = 'Wing Segment'
    airfoil: rcf.Components.Airfoil = field(default_factory=lambda: rcf.Components.Airfoil.NACA_4_Series(2412))

    # Specialty Attributes

    thickness_to_chord: float = 0.0
    percent_span_location: float = 0.0
    twist: float = 0.0
    dihedral_outboard: float = 0.0

    sweeps: rcf.ComponentDimensions()

    def __post_init__(self):
        self.sweeps.leading_edge = None
        self.sweeps.quarter_chord = 0.0
        self.sweeps.half_chord = 0.0







