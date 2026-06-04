# ----------------------------------------------------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------------------------------------------------

import subprocess
import os
import re

from pathlib import Path

import jax
import jax.numpy as jnp
import equinox as eqx
import plotly.graph_objects as go
import numpy as np

from tqdm import trange
from plotly.subplots import make_subplots

import RCAIDE.utils as ru

from RCAIDE.Library import Units
from RCAIDE.Library.Components import ComponentAreas
from RCAIDE.Library.Components.Wings import Wing, WingSegment, WingChords, WingDimensions, WingSweeps
from RCAIDE.Library.Components.Airfoils import Airfoil

from RCAIDE.Framework import Process, State, Settings, GradientMap
from RCAIDE.Framework.System import Aircraft
from RCAIDE.Framework.Missions.Conditions import Numerics

from RCAIDE.Framework.Analyses.Aerodynamics import VLM, VLMSettings, InitializeVLM, VLMVortices, SupersonicSettings

from RCAIDE.Framework.Interfaces.AVL import parse_avl_file, convert_to_RCAIDE
from RCAIDE.Framework.Plotting import plot_vlm_panels

# AVL Helper Functions -------------------------------------------------------------------------------------------------

def AVL_straight_wing(filename, name="Test_Wing", span=10.0, chord=1.0):
    """Writes a simple rectangular wing .avl file."""

    # Global Reference Values
    sref = span * chord
    cref = chord
    bref = span
    xref, yref, zref = 0.0, 0.0, 0.0

    # We define the right half of the wing, so semi-span is span/2
    semi_span = span / 2.0

    avl_text = f"""{name}
#Mach
0.0
#IYsym   IZsym   Zsym
 0       0       0.0
#Sref    Cref    Bref
 {sref}  {cref}  {bref}
#Xref    Yref    Zref
 {xref}  {yref}  {zref}

#======================================================
SURFACE
Main_Wing
#Nchordwise  Cspace  Nspanwise  Sspace
 12          0.0     20         0.0

YDUPLICATE
0.0

#------------------------------------------------------
SECTION
#Xle    Yle    Zle     Chord   Ainc  Nspanwise  Sspace
 0.0    0.0    0.0     {chord}   0.0   0          0

SECTION
#Xle    Yle     Zle    Chord   Ainc  Nspanwise  Sspace
 0.0  {semi_span} 0.0  {chord}   0.0   0          0
"""
    with open(filename, 'w') as f:
        f.write(avl_text)


def run_AVL_alpha_sweep(avl_file, alpha, run_name, oper_mode="st"):
    """Executes AVL silently using subprocess and a keystroke macro."""

    file_name = f"{run_name}_{oper_mode}.txt"

    # This string represents the EXACT keystrokes you would type in the terminal
    keystrokes = f"""load {avl_file}
oper
a
a
{alpha}
x
{oper_mode}
{file_name}
O

quit
"""
    # The 'O' above tells AVL to Overwrite the file if it already exists
    # The '\n' drops us out of the OPER menu back to the main menu

    avl_exe = os.path.expanduser("~/.local/bin/avl")
    print(f"\nRunning AVL for {avl_file} at Alpha = {alpha}...")

    # Call AVL natively from your PATH, piping the keystrokes in
    try:
        result = subprocess.run(
            [avl_exe],
            input=keystrokes,
            text=True,
            capture_output=True,
            timeout=5.0
        )
    except subprocess.TimeoutExpired:
        print("CRITICAL: AVL hung in an infinite loop and was terminated.")
        # You can optionally run a system kill command here just to be safe
        os.system("pkill -9 avl")
        return

    # Optional: Check if AVL crashed or threw a Fortran error
    if "Stop" in result.stdout or result.returncode != 0:
        print("AVL encountered an error!")
        print(result.stdout)

    print(f"Done. Saved stability data to {file_name}")


def parse_avl_stability(stab_file_path):
    """
    Parses an AVL stability (.st) output file and returns a dictionary
    of the core aerodynamic coefficients and stability derivatives.
    """
    results = {}

    with open(stab_file_path, 'r') as f:
        text = f.read()

    # 1. Parse Global Core Coefficients (e.g., CLtot =  0.34980)
    # The regex \s*=\s* handles any number of spaces around the equals sign
    # The ([-.\d]+) captures the actual number, including negatives and decimals
    core_keys = ['Alpha', 'CLtot', 'CDtot', 'Cmtot']
    for key in core_keys:
        match = re.search(fr"{key}\s*=\s*([-.\d]+)", text)
        if match:
            results[key] = float(match.group(1))

    # 2. Parse Stability Derivatives (e.g., CLa   4.500000)
    # Derivatives in AVL don't have an equals sign, just spaces
    # Example format: " CLa      4.500000"
    deriv_keys = ['CLa', 'Cma', 'Clb', 'Cnb', 'Cmq', 'Cnr']
    for key in deriv_keys:
        # Look for the key, followed by spaces, then capture the number
        match = re.search(fr"\b{key}\s+([-.\d]+)", text)
        if match:
            results[key] = float(match.group(1))

    return results

def AVL_basic_test(geometry_file=None, run_name=None, oper_mode="st", alpha=2.0, span=10.0, chord=1.0):
    # 1. Generate the geometry file
    if geometry_file is None:
        AVL_straight_wing(geometry_file, span=span, chord=chord)
        geometry_file = f"{run_name}.avl"

    if run_name is None:
        run_name = Path(geometry_file).stem

    run_AVL_alpha_sweep(geometry_file, alpha=alpha, run_name=run_name, oper_mode=oper_mode)

    if oper_mode == "st":
        parsed_data = parse_avl_stability(f"{run_name}_{oper_mode}.txt")

        print("\n--- Extracted AVL Results ---")
        for k, v in parsed_data.items():
            print(f"{k}: {v}")
        print("\n")


# VORJAX Helper Functions ----------------------------------------------------------------------------------------------

def VORJAX_straight_wing(span=10.0, chord=1.0):

    wing_spans = WingDimensions(projected=span)

    wing_chords = WingChords(root=chord, tip=chord, mean_aerodynamic=chord)

    wing_areas = ComponentAreas(reference=span * chord, wetted=2 * span * chord)

    wing = Wing(
        symmetric=True,
        spans=wing_spans,
        chords=wing_chords,
        areas=wing_areas,
        origin=jnp.array([[0.0, 0.0, 0.0]]),
        aerodynamic_center=jnp.array([0.0, 0.0, 0.0])
    )

    system = Aircraft(tag='Test Aircraft', areas=wing_areas).add_subcomponent(wing)
    system = eqx.tree_at(lambda s: s.mass_properties.center_of_gravity, system, jnp.array([[0.0, 0.0, 0.0]]))

    return system

def VORJAX_elliptical_wing(AR=10., n_segments=1):

    span = AR
    c_root = (4.0 * span) / (jnp.pi * AR)
    S_ref = span**2 / AR

    def chord_frac_at_eta(eta):
        # Using 0.99999 to prevent divide-by-zero or NaNs at the absolute tip
        return jnp.sqrt(1.0 - jnp.clip(eta, 0.0, 0.99999)**2)
    
    segments = ()
    eta = jnp.cos(jnp.linspace(jnp.pi/2, 0, n_segments + 1))
    
    for i in range(n_segments):
        eta_start = eta[i]
        eta_end   = eta[i+1]
        
        chord_frac_start = chord_frac_at_eta(eta_start)
        chord_frac_end   = chord_frac_at_eta(eta_end)

        # 1. Calculate the required setback of the quarter-chord
        # (Positive delta_x means the c/4 line is moving backward/sweeping aft)
        delta_x_c4 = 0.25 * 1.0 * (chord_frac_start - chord_frac_end) 
        
        # 2. Calculate the spanwise distance of this segment
        delta_y = 0.5 * AR * (eta_end - eta_start)
        
        # 3. Get the sweep angle
        sweep_c4 = jnp.arctan2(delta_x_c4, delta_y)

        segments += (WingSegment(
            tag=f"{i}", 
            percent_span_location=eta_start, 
            root_chord_percent=chord_frac_start,
            sweeps=WingSweeps(quarter_chord=sweep_c4)  # Inject sweep here!
        ),)

    # Tip segment doesn't need a sweep since there's no geometry after it
    segments += (WingSegment(
        tag="Tip", 
        percent_span_location=1.0, 
        root_chord_percent=0.01
    ),)

    wing_areas = ComponentAreas(reference=S_ref, wetted=2.0 * S_ref)

    wing = Wing(tag=f"Elliptical {n_segments}",
                segments=segments,
                symmetric=True,
                spans=WingDimensions(projected=span),
                chords=WingChords(root=c_root, tip=0.01 * c_root, mean_aerodynamic=c_root * 8.0 / (3 * jnp.pi)),
                areas=wing_areas,
                taper=0.01,
                origin=jnp.array([[0.0, 0.0, 0.0]]),
                aerodynamic_center=jnp.array([0.0, 0.0, 0.0])).update_geometry()
    
    system = Aircraft(tag='Test Aircraft', areas=wing_areas).add_subcomponent(wing)
    system = eqx.tree_at(lambda s: s.mass_properties.center_of_gravity, system, jnp.array([[0.0, 0.0, 0.0]]))

    return system  

def VORJAX_delta_wing(AR=2.0):
    
    # Define a fixed span, calculate the rest
    span = 10.0
    S_ref = span**2 / AR
    c_root = 2.0 * S_ref / span
    
    # Prevent divide-by-zero singularities at the tip
    c_tip_ratio = 0.001 
    
    # Calculate Quarter-Chord Sweep for a straight trailing edge
    # tan(sweep) = (0.75 * c_root) / (span / 2)
    sweep_c4 = jnp.arctan((0.75 * c_root) / (span / 2.0))
    
    segments = (
        WingSegment(
            tag="Root_to_Tip",
            percent_span_location=0.0,
            root_chord_percent=1.0,
            sweeps=WingSweeps(quarter_chord=sweep_c4)
        ),
        WingSegment(
            tag="Tip",
            percent_span_location=1.0,
            root_chord_percent=c_tip_ratio
        )
    )

    wing_areas = ComponentAreas(reference=S_ref, wetted=2.0 * S_ref)

    wing = Wing(tag=f"Delta_AR_{AR}",
                segments=segments,
                symmetric=True,
                spans=WingDimensions(projected=span),
                chords=WingChords(root=c_root, tip=c_root * c_tip_ratio, mean_aerodynamic=2.0/3.0 * c_root),
                areas=wing_areas,
                taper=c_tip_ratio,
                origin=jnp.array([[0.0, 0.0, 0.0]]),
                aerodynamic_center=jnp.array([0.0, 0.0, 0.0])).update_geometry()
    
    system = Aircraft(tag='Delta Aircraft', areas=wing_areas).add_subcomponent(wing)
    system = eqx.tree_at(lambda s: s.mass_properties.center_of_gravity, system, jnp.array([[0.0, 0.0, 0.0]]))

    return system

def VORJAX_ONERA_M6():
    """
    ONERA M6 Geometry Definition.
    src: https://www.grc.nasa.gov/www/wind/valid/m6wing/m6wing.html
    """

    AR = 3.8
    taper = 0.56
    
    sweep_qc = 26.7 * Units.deg
    sweep_le = 30.0 * Units.deg
    sweep_te = 15.8 * Units.deg

    c_root = 805.9 * Units.mm
    semispan = 1196.3 * Units.mm

    mac = 0.64607 * Units.m

    segments = (
        WingSegment(
            tag="ONERA M6",
            percent_span_location=0.0,
            root_chord_percent=1.0,
            sweeps=WingSweeps(leading_edge=sweep_le, quarter_chord=sweep_qc),
            airfoil=Airfoil.from_file("/home/jordan/dev/RCAIDE/Templates/Tests/VORJAX/SU2 Test Cases/onera_airfoil.txt")
        ),
        WingSegment(
            tag="Tip",
            percent_span_location=1.0,
            root_chord_percent=taper,
            airfoil=Airfoil.from_file("/home/jordan/dev/RCAIDE/Templates/Tests/VORJAX/SU2 Test Cases/onera_airfoil.txt")
        )
    )
    
    onera_wing = Wing(
        tag="Main Wing",
        symmetric=True,
        segments=segments,
        aspect_ratio=AR,
        taper=0.56,
        origin=jnp.array([[0.0, 0.0, 0.0]]),
        chords=WingChords(root=c_root, mean_aerodynamic=mac),
        spans=WingDimensions(projected=2 * semispan),
    ).update_geometry(calculate_reference_area=True, calculate_wetted_area=True)

    system = Aircraft(tag='ONERA M6 Container', areas=onera_wing.areas).add_subcomponent(onera_wing)
    system = eqx.tree_at(lambda s: s.mass_properties.center_of_gravity, system, jnp.array([[0.0, 0.0, 0.0]]))

    return system

def VORJAX_test_run(vehicle, alpha, Mach, n_sw=20, n_cw=6, grad_map=None, debug_mode=False):

    state = State(numerics=Numerics(number_of_control_points=1, calculate_integration=False))
    frozen_initials = eqx.tree_at(lambda s: s.initials, state, None, is_leaf=lambda x: x is None)
    state = eqx.tree_at(lambda s: s.initials, state, frozen_initials, is_leaf=lambda x: x is None)

    # Set State Values
    initial_state = eqx.tree_at(
        lambda s: (s.stability.static.roll_rate, s.stability.static.pitch_rate, s.stability.static.yaw_rate),
        state,
        (jnp.zeros((1, 1)), jnp.zeros((1, 1)), jnp.zeros((1, 1)))
    )

    if isinstance(alpha, list | jnp.ndarray) and isinstance(Mach, list | jnp.ndarray):
        assert len(alpha) == len(Mach)
        alpha = jnp.array(alpha).reshape(-1, 1)
        Mach = jnp.array(Mach).reshape(-1, 1)
    else:
        alpha = jnp.array([alpha])
        Mach = jnp.array([Mach])
    
    initial_state = eqx.tree_at(lambda s: s.aerodynamics.angles.alpha, initial_state, alpha)
    initial_state = eqx.tree_at(lambda s: s.freestream.mach_number, initial_state, Mach)

    initial_state = eqx.tree_at(lambda s: s.freestream.speed, initial_state, jnp.array([100.0]))
    initial_state = eqx.tree_at(lambda s: s.freestream.density, initial_state, jnp.array([1.0]))
    initial_state = eqx.tree_at(lambda s: s.freestream.temperature, initial_state, jnp.array([273.15]))
    initial_state = eqx.tree_at(lambda s: s.frames.inertial.velocity_vector, initial_state, jnp.array([100.0, 0., 0.]))

    initial_state = initial_state.expand_rows(len(alpha))

    initial_system = vehicle

    vortices = VLMVortices(
        spanwise_cosine_spacing=True,
        spanwise_vortices=n_sw,
        chordwise_vortices=n_cw
    )

    mach_settings = SupersonicSettings(
        peak_mach_number = 2.0,
        begin_blend_mach=0.7,
        end_blend_mach=1.2
    )
    
    aero_settings = VLMSettings(vortices=vortices, supersonic=mach_settings, le_suction_correction=True)
    initial_settings = eqx.tree_at(lambda s: s.analysis.aerodynamics, Settings(DEBUG_MODE=debug_mode), aero_settings)

    analysis = Process(
        tag="VORJAX Test Run",
        steps=(
            InitializeVLM(),
            VLM()
        ),
        initial_state=initial_state,
        initial_system=initial_system,
        initial_settings=initial_settings
    )

    results = analysis.run(
        initial_state,
        initial_system,
        initial_settings,
        grad_map=grad_map
    )

    return results

# Plotting Helper Functions ----------------------------------------------------------------------------------------------

def plot_elliptical_convergence_plotly(n_segments, grad_AD, error, grad_truth):
    
    # 1. Initialize figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Convert error to a percentage for cleaner reading
    error_percent = np.array(error) * 100.0

    # 2. Add Trace: AD Gradient (Primary Y)
    fig.add_trace(
        go.Scatter(
            x=n_segments, 
            y=grad_AD, 
            name="VORJAX AD Gradient",
            mode="lines+markers",
            line=dict(color="#1f77b4", width=3),
            marker=dict(size=8)
        ),
        secondary_y=False,
    )

    # 3. Add Trace: Analytical Truth (Primary Y)
    # Drawing a line from the first to the last x-coordinate
    fig.add_trace(
        go.Scatter(
            x=[n_segments[0], n_segments[-1]],
            y=[grad_truth, grad_truth],
            name="Analytical Truth",
            mode="lines",
            line=dict(color="black", width=3, dash="dash")
        ),
        secondary_y=False,
    )

    # 4. Add Trace: Relative Error (Secondary Y)
    fig.add_trace(
        go.Scatter(
            x=n_segments, 
            y=error_percent, 
            name="Relative Error",
            mode="lines+markers",
            line=dict(color="#d62728", width=3),
            marker=dict(symbol="square", size=8)
        ),
        secondary_y=True,
    )

    # 5. Styling and Layout
    fig.update_layout(
        title_text="<b>Elliptical Wing Grid Convergence: VORJAX vs. Lifting-Line Theory</b>",
        title_x=0.5,
        template="plotly_white",
        hovermode="x unified", # Combines all hover info into one box
        legend=dict(
            x=0.75,
            y=0.5,
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="black",
            borderwidth=1
        ),
        margin=dict(l=60, r=60, t=80, b=60)
    )

    # Format X-axis (Force integer ticks)
    fig.update_xaxes(
        title_text="<b>Number of Spanwise Segments</b>", 
        tickmode="linear", 
        tick0=0, 
        dtick=2,
        showgrid=True,
        gridcolor="lightgrey"
    )

    # Format Primary Y-axis
    fig.update_yaxes(
        title_text="<b>Autodiff Gradient (C<sub>L&alpha;</sub>) [rad<sup>-1</sup>]</b>", 
        color="#1f77b4",
        secondary_y=False,
        showgrid=True,
        gridcolor="lightgrey",
        zeroline=False,
        rangemode="tozero"

    )

    # Format Secondary Y-axis
    fig.update_yaxes(
        title_text="<b>Relative Error [%]</b>", 
        color="#d62728",
        secondary_y=True,
        showgrid=False, # Disabled to prevent clashing with primary gridlines
        zeroline=False,
        rangemode="tozero"
    )

    fig.show()

def plot_fd_v_curve_plotly(step_sizes, fd_errors):
    
    fig = go.Figure()

    # 1. Add Trace: FD Absolute Error
    fig.add_trace(
        go.Scatter(
            x=step_sizes, 
            y=fd_errors, 
            name="Central Difference Error",
            mode="lines+markers",
            line=dict(color="#9467bd", width=3),  # Muted purple
            marker=dict(symbol="circle", size=8),
            hovertemplate='Step Size (h): %{x:.1e}<br>Absolute Error: %{y:.1e}<extra></extra>'
        )
    )

    # 2. Add an invisible "floor" trace just to show where AD lives (machine zero)
    # This emphasizes that AD doesn't have a step size; it just sits at ~0 error.
    fig.add_trace(
        go.Scatter(
            x=[min(step_sizes), max(step_sizes)],
            y=[1e-16, 1e-16],
            name="VORJAX AD Error Bound (Machine Zero)",
            mode="lines",
            line=dict(color="black", width=2, dash="dot"),
            hoverinfo="skip"
        )
    )

    # 3. Styling and Layout
    fig.update_layout(
        title_text="<b>Finite Difference vs. Autodiff: The Step-Size Dilemma</b>",
        title_x=0.5,
        template="plotly_white",
        hovermode="x unified",
        legend=dict(
            x=0.5,
            y=1.05,
            xanchor="center",
            yanchor="bottom",
            orientation="h",
            bgcolor="rgba(255, 255, 255, 0.9)"
        ),
        margin=dict(l=60, r=60, t=100, b=60)
    )

    # 4. Format X-axis (Log Scale)
    fig.update_xaxes(
        title_text="<b>Finite Difference Step Size (h)</b>", 
        type="log",
        exponentformat="e",
        showgrid=True,
        gridcolor="lightgrey",
        # Ascending order is standard (1e-15 -> 1e-1)
        autorange="reversed" if step_sizes[0] > step_sizes[-1] else True 
    )

    # 5. Format Y-axis (Log Scale)
    fig.update_yaxes(
        title_text="<b>Absolute Error vs. AD Gradient</b>", 
        type="log",
        exponentformat="e",
        showgrid=True,
        gridcolor="lightgrey"
    )

    # 6. Educational Annotations
    # Floating on the left side (Round-off region)
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.05, y=0.85,
        text="<b>Round-off Error</b><br>Dominates",
        showarrow=False,
        font=dict(color="#d62728", size=13),
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#d62728",
        borderwidth=1
    )

    # Floating on the right side (Truncation region)
    fig.add_annotation(
        xref="paper", yref="paper",
        x=0.95, y=0.85,
        text="<b>Truncation Error</b><br>Dominates",
        showarrow=False,
        font=dict(color="#1f77b4", size=13),
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#1f77b4",
        borderwidth=1
    )

    fig.show()

def plot_theoretical_error_comparison_plotly(step_sizes, fd_grads, exact_grad, grad_truth):
    
    # Calculate Relative Errors against Lifting-Line Theory
    fd_rel_errors = np.abs((np.array(fd_grads) - grad_truth) / grad_truth)
    ad_rel_error = float(np.abs((np.asarray(exact_grad) - grad_truth) / grad_truth))

    fig = go.Figure()

    # 1. Add Trace: FD Relative Error vs Theory
    fig.add_trace(
        go.Scatter(
            x=step_sizes, 
            y=fd_rel_errors, 
            name="Finite Difference Error",
            mode="lines+markers",
            line=dict(color="#d62728", width=3),  # Red
            marker=dict(symbol="circle", size=8),
            hovertemplate='Step Size (h): %{x:.1e}<br>FD Rel Error: %{y:.2e}<extra></extra>'
        )
    )

    # 2. Add Trace: AD Relative Error vs Theory (Flat Line)
    fig.add_trace(
        go.Scatter(
            x=[min(step_sizes), max(step_sizes)],
            y=[ad_rel_error, ad_rel_error],
            name=f"Autodiff Error Floor (Grid Limit)",
            mode="lines",
            line=dict(color="#1f77b4", width=3, dash="dash"), # Blue dashed
            hovertemplate=f'AD Rel Error (No Step Size): {ad_rel_error:.2e}<extra></extra>'
        )
    )

    # 3. Styling and Layout
    fig.update_layout(
        title_text="<b>Gradient Accuracy vs. Lifting-Line Theory</b>",
        title_x=0.5,
        template="plotly_white",
        hovermode="x unified",
        legend=dict(
            x=0.5,
            y=1.05,
            xanchor="center",
            yanchor="bottom",
            orientation="h",
            bgcolor="rgba(255, 255, 255, 0.9)"
        ),
        margin=dict(l=60, r=60, t=100, b=60)
    )

    # 4. Format X-axis (Log Scale)
    fig.update_xaxes(
        title_text="<b>Finite Difference Step Size (h)</b>", 
        type="log",
        exponentformat="e",
        showgrid=True,
        gridcolor="lightgrey",
        autorange="reversed" if step_sizes[0] > step_sizes[-1] else True 
    )

    # 5. Format Y-axis (Log Scale)
    fig.update_yaxes(
        title_text="<b>Relative Error vs. Theoretical Truth</b>", 
        type="log",
        exponentformat="e",
        showgrid=True,
        gridcolor="lightgrey"
    )

    # 6. Annotations
    fig.add_annotation(
        x=np.log10(step_sizes[len(step_sizes)//2]), # Middle of the plot
        y=np.log10(ad_rel_error),
        text="VLM Grid Discretization Limit",
        showarrow=True,
        arrowhead=2,
        ax=0,
        ay=-40,
        font=dict(color="#1f77b4", size=12)
    )

    fig.show()

def plot_delta_ar_sweep_plotly(ARs, grad_AD, error_AD, grad_jones, grad_FD=None, error_FD=None):
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # --- Primary Y: Gradients ---
    fig.add_trace(
        go.Scatter(
            x=ARs, y=grad_AD, 
            name="VORJAX AD Gradient",
            mode="lines+markers",
            line=dict(color="#1f77b4", width=3),
            marker=dict(symbol="circle", size=8)
        ), secondary_y=False
    )
    
    if grad_FD is not None and len(grad_FD) > 0:
        fig.add_trace(
            go.Scatter(
                x=ARs, y=grad_FD, 
                name="Central Difference (FD)",
                mode="markers",
                marker=dict(color="orange", symbol="x", size=8, line=dict(width=2))
            ), secondary_y=False
        )

    fig.add_trace(
        go.Scatter(
            x=ARs, y=grad_jones, 
            name="Jones Slender Wing Theory",
            mode="lines",
            line=dict(color="black", width=3, dash="dash")
        ), secondary_y=False
    )

    # --- Secondary Y: Errors ---
    error_AD_pct = np.array(error_AD) * 100.0
    fig.add_trace(
        go.Scatter(
            x=ARs, y=error_AD_pct, 
            name="AD Relative Error vs Jones",
            mode="lines+markers",
            line=dict(color="#d62728", width=2, dash="dot"),
            marker=dict(symbol="square", size=6)
        ), secondary_y=True
    )

    if error_FD is not None and len(error_FD) > 0:
        error_FD_pct = np.array(error_FD) * 100.0
        fig.add_trace(
            go.Scatter(
                x=ARs, y=error_FD_pct, 
                name="FD Relative Error vs Jones",
                mode="lines+markers",
                line=dict(color="orange", width=2, dash="dot"),
                marker=dict(symbol="x", size=6)
            ), secondary_y=True
        )

    # --- Layout & Styling ---
    fig.update_layout(
        title_text="<b>Delta Wing Aspect Ratio Sweep: VLM vs. Slender Wing Theory</b>",
        title_x=0.5,
        template="plotly_white",
        hovermode="x unified",
        legend=dict(x=0.02, y=0.98, bgcolor="rgba(255, 255, 255, 0.9)", bordercolor="black", borderwidth=1),
        margin=dict(l=60, r=60, t=80, b=60)
    )

    fig.update_xaxes(title_text="<b>Aspect Ratio (AR)</b>", showgrid=True, gridcolor="lightgrey")
    fig.update_yaxes(title_text="<b>Gradient (C<sub>L&alpha;</sub>) [rad<sup>-1</sup>]</b>", 
                     color="#1f77b4", secondary_y=False, showgrid=True, gridcolor="lightgrey", rangemode="tozero")
    fig.update_yaxes(title_text="<b>Relative Error [%]</b>", 
                     color="#d62728", secondary_y=True, showgrid=False, rangemode="tozero")

    return fig

def plot_delta_convergence_and_memory_plotly(n_panels, grad_AD, memory_gb, grad_truth):
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # --- Primary Y: AD Gradient Convergence ---
    fig.add_trace(
        go.Scatter(
            x=n_panels, 
            y=grad_AD, 
            name="VORJAX AD Gradient",
            mode="lines+markers",
            line=dict(color="#1f77b4", width=3), # Blue
            marker=dict(size=8),
            hovertemplate='Panels: %{x}<br>Gradient: %{y:.4f}<extra></extra>'
        ), secondary_y=False
    )

    # Primary Y: Truth Line
    fig.add_trace(
        go.Scatter(
            x=[n_panels[0], n_panels[-1]], 
            y=[grad_truth, grad_truth],
            name="Jones Theory Truth",
            mode="lines",
            line=dict(color="black", width=3, dash="dash"),
            hoverinfo="skip"
        ), secondary_y=False
    )

    # --- Secondary Y: VRAM Memory Usage ---
    fig.add_trace(
        go.Scatter(
            x=n_panels, 
            y=memory_gb, 
            name="Peak VRAM Allocation",
            mode="lines+markers",
            line=dict(color="#2ca02c", width=3), # Green
            marker=dict(symbol="square", size=8),
            hovertemplate='Panels: %{x}<br>VRAM: %{y:.2f} GB<extra></extra>'
        ), secondary_y=True
    )

    # --- Layout & Styling ---
    fig.update_layout(
        title_text="<b>Delta Wing: Gradient Convergence vs. Memory Cost</b>",
        title_x=0.5,
        template="plotly_white",
        hovermode="x unified",
        legend=dict(
            x=0.05, y=0.5, 
            bgcolor="rgba(255, 255, 255, 0.9)", 
            bordercolor="black", borderwidth=1
        ),
        margin=dict(l=60, r=60, t=80, b=60)
    )

    # Format X-axis (Log Scale for doubling panels)
    fig.update_xaxes(
        title_text="<b>Number of Panels (N)</b>", 
        type="log",
        tickvals=n_panels, # Force ticks only on the values you tested
        ticktext=[str(val) for val in n_panels],
        showgrid=True, 
        gridcolor="lightgrey"
    )
    
    # Format Primary Y-axis (Linear for Gradient)
    fig.update_yaxes(
        title_text="<b>Gradient (C<sub>L&alpha;</sub>) [rad<sup>-1</sup>]</b>", 
        color="#1f77b4", 
        secondary_y=False, 
        showgrid=True, 
        gridcolor="lightgrey", 
    )
    
    # Format Secondary Y-axis (Log Scale for O(N^2) memory)
    fig.update_yaxes(
        title_text="<b>Peak GPU Memory [GB]</b>", 
        color="#2ca02c", 
        type="log",
        secondary_y=True, 
        showgrid=False # Disabled to prevent gridline clashing
    )

    return fig

# Execution ------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":


    # geometry_file = '/home/jordan/dev/RCAIDE/Templates/Tests/V_and_V/AVL Test Cases/b737_wings_flat_no_af.avl'

    # avl_b737_data = parse_avl_file(Path(geometry_file))
    # vehicle = convert_to_RCAIDE(avl_b737_data)
    

    # AVL_basic_test(geometry_file, oper_mode="st")

    alpha_path = ru.PathTuple(("aerodynamics", "angles", "alpha"))
    lift_path = ru.PathTuple(("aerodynamics", "coefficients", "lift", "total"))

    grad_map = GradientMap(
        state_inputs=(alpha_path,),
        state_outputs=(lift_path,)
    )

    TEST_ELLIPTICAL = False
    TEST_DELTA = False
    TEST_ONERA = True
    
    PLOT_WINGS = True
    
    DEBUG = True

    # Elliptical Wing Test ---------------------------------------------------------------------------------------------
    if TEST_ELLIPTICAL:

        max_segments = 20
        AR = 10.0
        grad_truth = 2.0 * jnp.pi/(1 + 2 / AR)
        step_sizes = jnp.logspace(-1, -15, 15)
        
        CL = []
        grad_AD = []
        error_AD = []
        
        grad_FD = []
        error_FD = []

        # vehicle = VORJAX_straight_wing(span=10.0, chord=1.0)
        for n_seg in trange(1, max_segments+1, desc="Running Elliptical Test Cases"):
            vehicle = VORJAX_elliptical_wing(AR=AR, n_segments=n_seg)

            results = VORJAX_test_run(vehicle, alpha=2.0 * Units.deg , Mach=0.00, grad_map=grad_map, debug_mode=DEBUG)
            f_st, f_sys, f_setts, jac = results

            CL.append(ru.get_target(f_st, lift_path).item(0))
            grad_AD.append(jac.item(0))
            error_AD.append(abs(jac.item(0) - grad_truth)/grad_truth)

            if PLOT_WINGS:
                if n_seg % 5 == 0:
                    fig = plot_vlm_panels(VD=f_sys.analysis_data['vortex_distribution'])
                    fig.show()
            
        vehicle = VORJAX_elliptical_wing(AR=AR, n_segments=max_segments)
        for i in trange(len(step_sizes), desc="Running Elliptical FD Tests"):
            h = step_sizes[i]

            # Forward Step
            res_fwd = VORJAX_test_run(vehicle, alpha=(2.0 * Units.deg) + h, Mach=0.00, debug_mode=DEBUG)
            CL_fwd = ru.get_target(res_fwd[0], lift_path).item(0)
            
            # Backward Step
            res_bwd = VORJAX_test_run(vehicle, alpha=(2.0 * Units.deg) - h, Mach=0.00, debug_mode=DEBUG)
            CL_bwd = ru.get_target(res_bwd[0], lift_path).item(0)
            
            # Central Difference
            g_FD = (CL_fwd - CL_bwd) / (2 * h)
            grad_FD.append(g_FD)
            
            # Calculate absolute error against JAX
            error_FD.append(abs(g_FD - grad_AD[-1]))

        n_segments_list = list(range(1, max_segments+1))
        plot_elliptical_convergence_plotly(n_segments_list, grad_AD, error_AD, grad_truth)
        plot_fd_v_curve_plotly(step_sizes, error_FD)
        plot_theoretical_error_comparison_plotly(step_sizes, grad_FD, grad_AD[-1], grad_truth)

    # Delta Wing Test --------------------------------------------------------------------------------------------------
    if TEST_DELTA:
        CL = []
        grad_AD = []
        error_AD = []

        vram_gb = []

        ARs = jnp.linspace(0.1, 2.5, 25)
        grad_jones = jnp.pi * ARs / 2.0
        step_sizes = jnp.logspace(-1, -15, 15)

        n_cws   = [4, 8, 8, 16, 16, 32, 32, 64, 64]
        n_sws   = [4, 4, 8, 8,  16, 16, 32, 32, 64]

        vehicle = VORJAX_delta_wing(AR=ARs[0])
        for i in trange(len(n_sws), desc="Running Delta Wing Panelization Tests"):
            n_sw = n_sws[i]
            n_cw = n_cws[i]

            # Forward Step
            results = VORJAX_test_run(vehicle, alpha=2.0 * Units.deg, Mach=0.00, n_sw=n_sw, n_cw=n_cw, grad_map=grad_map, debug_mode=DEBUG)
            f_st, f_sys, f_setts, jac = results

            jac.block_until_ready()
            stats = jax.devices()[0].memory_stats()
            peak_vram = stats.get('peak_bytes_in_use', 0) / (1024 ** 3)
            vram_gb.append(peak_vram)
            
            CL.append(ru.get_target(f_st, lift_path).item(0))
            grad_AD.append(jac.item(0))
            error_AD.append(abs(jac.item(0) - grad_jones[0])/grad_jones[0])

        
        fig = plot_delta_convergence_and_memory_plotly([s * c for s, c in zip(n_sws, n_cws)], grad_AD, vram_gb, grad_jones[0])
        fig.show()

        CL = []
        grad_AD = []
        error_AD = []

        for i in trange(len(ARs), desc="Running Delta Wing Test Cases"):
            vehicle = VORJAX_delta_wing(AR=ARs[i])
            grad_truth = grad_jones[i]

            results = VORJAX_test_run(vehicle, alpha=2.0 * Units.deg , Mach=0.00, grad_map=grad_map, debug_mode=DEBUG)
            f_st, f_sys, f_setts, jac = results

            CL.append(ru.get_target(f_st, lift_path).item(0))
            grad_AD.append(jac.item(0))
            error_AD.append(abs(jac.item(0) - grad_truth)/grad_truth)

            if PLOT_WINGS:
                if int(i) % 10 == 0:
                    fig = plot_vlm_panels(f_sys.analysis_data['vortex_distribution'])
                    fig.show()
        
        fig = plot_delta_ar_sweep_plotly(ARs, grad_AD, error_AD, grad_jones)
        fig.show()
        
    # ONERA M6 Mach Sweep ----------------------------------------------------------------------------------------------
    if TEST_ONERA:
        
        alpha = [3.06 * Units.deg] * 21
        Mach =  [0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]

        alpha_path = ru.PathTuple(("aerodynamics", "angles", "alpha"))
        lift_path = ru.PathTuple(("aerodynamics", "coefficients", "lift", "total"))

        grad_map = GradientMap(
            state_inputs=(alpha_path,),
            state_outputs=(lift_path,)
        )

        vehicle = VORJAX_ONERA_M6()

        results = VORJAX_test_run(vehicle, alpha, Mach, n_sw=40, n_cw=12, grad_map=grad_map, debug_mode=DEBUG)
        f_st, f_sys, f_setts, jac = results


        CL = ru.get_target(f_st, lift_path)
        dCL_dAlpha = jnp.array([jac[i, 0, i] for i in range(21)]).reshape(CL.shape)

        print("\nONERA M6 Mach Sweep\n"+"-"*42)
        for i in range(CL.shape[0]):
            print(f"M: {Mach[i]: .2f}, CL: {float(CL[i, 0]):.3e}, dAlpha: {float(dCL_dAlpha[i, 0]):.3e}")

        if PLOT_WINGS:
            data = f_sys.analysis_data
            base_panels = plot_vlm_panels(data["vortex_distribution"], title="ONERA M6 Panelization")
            base_panels.show()

            # m03 = plot_vlm_panels(data["vortex_distribution"], data['singularities'][0], title="ONERA M6 DCp, M = 0.3")
            # m03.show()

            m11_flags = plot_vlm_panels(data["vortex_distribution"], data['singularities'][11], title="ONERA M6 Flag, M = 1.1")
            m11_flags.show()

            m11_dcp = plot_vlm_panels(data["vortex_distribution"], data['pressure_coefficients'][11], title="ONERA M6 DCp, M = 1.1")
            m11_dcp.show()

            # m20 = plot_vlm_panels(data["vortex_distribution"], data['singularities'][-1], title="ONERA M6 DCp, M = 2.0")
            # m20.show()


    print("Done!")