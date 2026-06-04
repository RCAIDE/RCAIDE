# RCAIDE/Framework/Components/Airfoil.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Sep 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from decimal import Decimal
from pathlib import Path
from os import path

# package imports
import equinox as eqx
import jax.numpy as jnp
from scipy.interpolate import PchipInterpolator

# RCAIDE imports
from RCAIDE.Library import Component

# ----------------------------------------------------------------------------------------------------------------------
#  Airfoil Data Locator
# ----------------------------------------------------------------------------------------------------------------------

Airfoil_Data = Path(path.join(path.dirname(__file__), 'Airfoil_Data'))

# ----------------------------------------------------------------------------------------------------------------------
#  Airfoil
# ----------------------------------------------------------------------------------------------------------------------

class Airfoil(Component):

    tag:                str = eqx.field(static=True, default="Airfoil")

    thickness_to_chord: float = 0.0
    max_thickness:      float = 0.0
    wedge_angle:        float = 0.0

    coordinates:        jnp.ndarray = eqx.field(default_factory=jnp.empty((0, 2)))

    camber:             jnp.ndarray = eqx.field(default_factory=jnp.empty((0)))

    x_coordinates:      jnp.ndarray = eqx.field(default_factory=jnp.empty((0)))
    y_coordinates:      jnp.ndarray = eqx.field(default_factory=jnp.empty((0)))
    
    x_upper_surface:    jnp.ndarray = eqx.field(default_factory=jnp.empty(0))
    x_lower_surface:    jnp.ndarray = eqx.field(default_factory=jnp.empty(0))
    
    y_upper_surface:    jnp.ndarray = eqx.field(default_factory=jnp.empty(0))
    y_lower_surface:    jnp.ndarray = eqx.field(default_factory=jnp.empty(0))

    @classmethod
    def NACA_4_Series(cls, series_number: str | int, n_pts: int = 201, edge_factor: float = 1.5):

        # Extract digits from series number

        if isinstance(series_number, str):
            digits = tuple(int(x) for x in series_number)
        elif isinstance(series_number, int):
            digits = Decimal(series_number).as_tuple().digits
        else:
            raise ValueError("NACA series number must be a string or an integer")

        assert len(digits) == 4, "NACA series number must be 4 digits long"

        # Correct number of points to ensure odd

        if n_pts % 2 == 0:
            n_pts += 1

        # Calculate parameters

        camber = digits[0] / 100
        camber_location = digits[1] / 10
        thickness = digits[2] / 10 + digits[3] / 100

        # Prepare upper and lower surfaces coordinates

        x_upper = jnp.linspace(0, 1, int(jnp.ceil(n_pts / 2)))
        x_lower = jnp.linspace(0, 1, int(jnp.ceil(n_pts / 2)))

        # Concentrate coordinates near edges

        if edge_factor:
            ef = edge_factor
            x_upper = 1 - (ef + 1) * x_upper * (1 - x_upper) ** ef - (1 - x_upper) ** (ef + 1)
            x_lower = 1 - (ef + 1) * x_lower * (1 - x_lower) ** ef - (1 - x_lower) ** (ef + 1)

        # Compute chordwise thickness distribution
        def _x2t(x):
            return (0.2969 * jnp.sqrt(x)
                    - 0.126 * x
                    - 0.3516 * (x ** 2)
                    + 0.2843 * (x ** 3)
                    - 0.1015 * (x ** 4)) * thickness / 0.2

        t_lower = _x2t(x_lower)
        t_upper = _x2t(x_upper)

        # Compute chordwise camber distribution
        def _x2c(x):
            return camber / (1 - camber_location) ** 2 * ((1 - 2 * camber_location) + 2 * camber_location * x - x ** 2)

        c_upper = _x2c(x_upper)
        c_lower = _x2c(x_lower)

        if camber and camber_location:

            def x2c_corrected(x, c):

                idx = jnp.where(x < camber_location)[0]
                c = c.at[idx].set(camber / camber_location ** 2 * (2 * camber_location * x[idx] - x[idx] ** 2))

                return c

            c_upper = x2c_corrected(x_upper, c_upper)
            c_lower = x2c_corrected(x_lower, c_lower)

        # Compute surface coordinates

        x_lo    = jnp.flip(x_lower)
        x_up    = x_upper[1:]
        x       = jnp.hstack((x_lo, x_up))

        y_lo    = jnp.flip(c_lower - t_lower)
        y_up    = (c_upper + t_upper)[1:]
        y       = jnp.hstack((y_lo, y_up))

        return cls(
            tag='NACA ' + str(series_number),
            camber=camber,
            max_thickness=thickness,
            thickness_to_chord=thickness / (max(x) - min(x)),
            coordinates=jnp.vstack((x, y)).T,
            x_coordinates=x,
            y_coordinates=y,
            x_upper_surface=x_up,
            x_lower_surface=x_lo,
            y_upper_surface=y_up,
            y_lower_surface=y_lo
        )

    @classmethod
    def from_file(cls, file_path: str | Path, n_pts: int = 101):
        """
        Parses Selig and Lednicer format airfoil .dat files.
        Interpolates upper and lower surfaces onto a shared cosine-spaced X grid
        to accurately calculate the mean camber line.
        """
        file_path = Path(file_path)

        # 1. Read all non-empty lines
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        is_lednicer = False
        data_start_idx = 0
        n_up, n_lo = 0, 0

        # 2. Format Detection
        # Lednicer files uniquely define the number of upper/lower points in the header
        # (e.g., "30.0  30.0" or "30  30")
        for i, line in enumerate(lines[:5]):
            parts = line.replace(',', ' ').split()
            if len(parts) == 2:
                try:
                    val1, val2 = float(parts[0]), float(parts[1])
                    # If both are > 1.5, it's a point count, not an x-coordinate
                    if val1 > 1.5 and val2 > 1.5:
                        is_lednicer = True
                        n_up, n_lo = int(val1), int(val2)
                        data_start_idx = i + 1
                        break
                except ValueError:
                    continue

        # If it's not Lednicer, it's Selig. Find the first line that is numeric coordinates.
        if not is_lednicer:
            for i, line in enumerate(lines):
                parts = line.replace(',', ' ').split()
                if len(parts) >= 2:
                    try:
                        float(parts[0]), float(parts[1])
                        data_start_idx = i
                        break
                    except ValueError:
                        continue

        # 3. Extract Raw Coordinates
        raw_coords = []
        for line in lines[data_start_idx:]:
            parts = line.replace(',', ' ').split()
            if len(parts) >= 2:
                try:
                    raw_coords.append([float(parts[0]), float(parts[1])])
                except ValueError:
                    continue

        raw_coords = jnp.array(raw_coords)
        x_raw, y_raw = raw_coords[:, 0], raw_coords[:, 1]

        # 4. Surface Splitting & Orientation (Force LE -> TE)
        if is_lednicer:
            # Lednicer: Upper first, then Lower. Both inherently LE -> TE.
            x_up, y_up = x_raw[:n_up], y_raw[:n_up]
            x_lo, y_lo = x_raw[n_up:n_up + n_lo], y_raw[n_up:n_up + n_lo]

        else:
            # Selig: TE -> Upper -> LE -> Lower -> TE
            le_idx = jnp.argmin(x_raw)

            x_up, y_up = x_raw[:le_idx + 1], y_raw[:le_idx + 1]
            x_lo, y_lo = x_raw[le_idx:], y_raw[le_idx:]

            # Reverse upper to make it LE -> TE
            x_up, y_up = x_up[::-1], y_up[::-1]

        # 5. Clean Duplicates and Enforce Strict Monotonicity for Interpolation
        def make_monotonic(x, y):
            # Finds unique X values and sorts them. (Since they go LE->TE, sorting is safe)
            x_unique, idx = jnp.unique(x, return_index=True)
            return x_unique, y[idx]

        x_up_clean, y_up_clean = make_monotonic(x_up, y_up)
        x_lo_clean, y_lo_clean = make_monotonic(x_lo, y_lo)

        # 6. Create Common X-Grid (Cosine Spacing for clustering at LE/TE)
        beta = jnp.linspace(0, jnp.pi, n_pts)
        common_x = 0.5 * (1.0 - jnp.cos(beta))

        # 7. Interpolate onto the Common Grid
        # We use PCHIP (Shape-preserving piecewise cubic) because standard cubic splines
        # tend to wildly overshoot and create "wiggles" near the blunt leading edge.
        y_up_interp = PchipInterpolator(x_up_clean, y_up_clean)(common_x)
        y_lo_interp = PchipInterpolator(x_lo_clean, y_lo_clean)(common_x)

        # Force LE to exactly (0, 0) and TE to exactly (1, y)
        y_up_interp[0], y_lo_interp[0] = 0.0, 0.0
        common_x = common_x.at[0].set(0.0)
        common_x = common_x.at[-1].set(1.0)

        # 8. Calculate Aerodynamic Properties
        camber = (y_up_interp + y_lo_interp) / 2.0
        thickness = y_up_interp - y_lo_interp
        max_t = jnp.max(thickness)
        t_c = max_t / 1.0

        # 9. Reconstruct the continuous loop for standard plotting (TE -> LE -> TE)
        x_loop = jnp.concatenate((common_x[::-1], common_x[1:]))
        y_loop = jnp.concatenate((y_up_interp[::-1], y_lo_interp[1:]))

        # 10. Cast back to JAX arrays and return the initialized class
        return cls(
            tag=file_path.stem,
            camber=jnp.array(camber),
            max_thickness=float(max_t),
            thickness_to_chord=float(t_c),
            coordinates=jnp.column_stack((jnp.array(x_loop), jnp.array(y_loop))),
            x_coordinates=jnp.array(x_loop),
            y_coordinates=jnp.array(y_loop),
            x_upper_surface=jnp.array(common_x),
            x_lower_surface=jnp.array(common_x),
            y_upper_surface=jnp.array(y_up_interp),
            y_lower_surface=jnp.array(y_lo_interp)
        )