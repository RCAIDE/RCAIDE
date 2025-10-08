# RCAIDE/Library/Plots/Geometry/generate_3d_lopa_points.py
#
# Created:  Jul 2023, M. Clarke
# Modified:  Mar 2025, Codex (business/economy VTK seats)

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORTS
# ----------------------------------------------------------------------------------------------------------------------
import sys
from typing import Optional

import numpy as np
import vtk
import matplotlib.colors as mcolors

from RCAIDE.Framework.Core import Data


# ----------------------------------------------------------------------------------------------------------------------
#  CONSTANTS
# ----------------------------------------------------------------------------------------------------------------------
DEFAULT_SEAT_HEIGHT = 0.45            # [m] nominal cushion height for visualization
DEFAULT_SEAT_CLEARANCE = 0.05         # [m] lift seats slightly above the cabin floor
SEAT_LENGTH_SCALE = 0.90              # shrink seat length to avoid overlap
SEAT_WIDTH_SCALE = 0.90               # shrink seat width to avoid overlap
MIN_DIMENSION = 1e-3                  # minimum dimension to keep VTK happy

BUSINESS_COLOR = mcolors.to_rgb("seagreen")
ECONOMY_COLOR = mcolors.to_rgb("steelblue")

_MAKE_OBJECT_PATCHED = False
_ORIGINAL_MAKE_OBJECT = None


# ----------------------------------------------------------------------------------------------------------------------
#  PUBLIC FUNCTION
# ----------------------------------------------------------------------------------------------------------------------
def generate_3d_lopa_points(structure, tessellation: int = 24):
    """Generate simple VTK seat geometry for Layout Of Passenger Accommodation (LOPA).

    The routine builds small cuboid "cushions" for each seat and stores them as
    polydata objects. Business-class seats are tinted green, economy seats blue.

    Parameters
    ----------
    structure : Fuselage | Wing | Data
        Vehicle structure containing layout_of_passenger_accommodations.
    tessellation : int, optional
        Unused. Kept for API compatibility with other geometry generators.

    Returns
    -------
    Data
        Data object with placeholder ``PTS`` (for compatibility) and a private
        ``_lopa_components`` list holding the VTK polydata plus color metadata.
    """

    _ensure_make_object_patch()

    seat_table = _extract_lopa_coordinates(structure)
    if seat_table is None or seat_table.size == 0:
        return _empty_geometry()

    seat_rows = seat_table[np.isclose(seat_table[:, 10], 1.0)]
    if seat_rows.size == 0:
        return _empty_geometry()

    seat_height = _resolve_seat_height(structure)
    seat_components = []
    business_count = 0
    economy_count = 0

    for row in seat_rows:
        if np.isclose(row[8], 1.0):
            color = BUSINESS_COLOR
            business_count += 1
        elif np.isclose(row[9], 1.0):
            color = ECONOMY_COLOR
            economy_count += 1
        else:
            # Skip first-class or other objects for now.
            continue

        center_x = float(row[2])
        center_y = float(row[3])
        base_z = float(row[4]) + DEFAULT_SEAT_CLEARANCE
        length = max(abs(float(row[5])) * SEAT_LENGTH_SCALE, MIN_DIMENSION)
        width = max(abs(float(row[6])) * SEAT_WIDTH_SCALE, MIN_DIMENSION)

        component = _create_seat_component(center_x=center_x,
                                           center_y=center_y,
                                           base_z=base_z,
                                           length=length,
                                           width=width,
                                           height=seat_height,
                                           color=color)
        seat_components.append(component)

    geometry = _empty_geometry()
    geometry._lopa_components = seat_components

    geometry.metadata = Data()
    geometry.metadata.business_seat_count = business_count
    geometry.metadata.economy_seat_count = economy_count

    return geometry


# ----------------------------------------------------------------------------------------------------------------------
#  HELPERS
# ----------------------------------------------------------------------------------------------------------------------
def _empty_geometry() -> Data:
    """Return an empty geometry container compatible with make_object."""

    geom = Data()
    # Placeholder array so callers expecting .PTS continue to work.
    geom.PTS = np.zeros((1, 1, 3))
    geom._lopa_components = []
    return geom


def _extract_lopa_coordinates(structure) -> Optional[np.ndarray]:
    """Safely extract the LOPA coordinate array from the provided structure."""

    layout = getattr(structure, "layout_of_passenger_accommodations", None)

    if layout is None:
        return None

    coords = None
    if isinstance(layout, Data) and hasattr(layout, "object_coordinates"):
        coords = layout.object_coordinates
    elif isinstance(layout, np.ndarray):
        coords = layout

    if coords is None:
        return None

    coords = np.asarray(coords, dtype=float)
    if coords.ndim != 2 or coords.shape[1] < 14:
        return None

    return coords


def _resolve_seat_height(structure) -> float:
    """Determine a reasonable seat height for visualization."""

    candidate = getattr(structure, "seat_height", None)
    try:
        seat_height = float(candidate)
    except (TypeError, ValueError):
        seat_height = DEFAULT_SEAT_HEIGHT

    if seat_height <= 0.0:
        seat_height = DEFAULT_SEAT_HEIGHT

    return seat_height


def _create_seat_component(center_x: float,
                           center_y: float,
                           base_z: float,
                           length: float,
                           width: float,
                           height: float,
                           color) -> dict:
    """Create a VTK cuboid representing a single seat."""

    cube = vtk.vtkCubeSource()
    cube.SetCenter(center_x, center_y, base_z + 0.5 * height)
    cube.SetXLength(max(length, MIN_DIMENSION))
    cube.SetYLength(max(width, MIN_DIMENSION))
    cube.SetZLength(max(height, MIN_DIMENSION))
    cube.Update()

    polydata = vtk.vtkPolyData()
    polydata.ShallowCopy(cube.GetOutput())

    return {
        "polydata": polydata,
        "color": color,
    }


def _ensure_make_object_patch():
    """Patch plot_3d_vehicle.make_object once to understand LOPA components."""

    global _MAKE_OBJECT_PATCHED, _ORIGINAL_MAKE_OBJECT

    if _MAKE_OBJECT_PATCHED:
        return

    module = sys.modules.get('RCAIDE.Library.Plots.Geometry.plot_3d_vehicle')
    if module is None:
        # The plot module is not yet imported; defer patching until later.
        return

    _ORIGINAL_MAKE_OBJECT = module.make_object

    def wrapped_make_object(renderer, geom, rgb_color=None, opacity=None):
        components = getattr(geom, "_lopa_components", None)

        if components is not None:
            base_opacity = _resolve_opacity(rgb_color, opacity)
            for component in components:
                polydata = component.get("polydata")
                if polydata is None:
                    continue

                mapper = vtk.vtkPolyDataMapper()
                mapper.SetInputData(polydata)

                actor = vtk.vtkActor()
                actor.SetMapper(mapper)

                color = component.get("color", (0.6, 0.6, 0.6))
                actor.GetProperty().SetColor(*color)
                actor.GetProperty().SetDiffuse(1.0)
                actor.GetProperty().SetSpecular(0.0)
                actor.GetProperty().SetOpacity(component.get("opacity", base_opacity))

                renderer.AddActor(actor)
            return

        # Fallback: support legacy three-argument usage where rgb_color is opacity.
        if opacity is None and not _is_rgb_sequence(rgb_color):
            default_color = (0.6, 0.6, 0.6)
            fallback_opacity = _resolve_opacity(rgb_color, opacity)
            _ORIGINAL_MAKE_OBJECT(renderer, geom, default_color, fallback_opacity)
            return

        resolved_opacity = 1.0 if opacity is None else float(opacity)
        _ORIGINAL_MAKE_OBJECT(renderer, geom, rgb_color, resolved_opacity)

    module.make_object = wrapped_make_object
    module._lopa_make_object_wrapped = True
    _MAKE_OBJECT_PATCHED = True


def _resolve_opacity(rgb_color_arg, opacity_arg) -> float:
    """Convert the incoming arguments into a usable opacity value."""

    if opacity_arg is not None:
        try:
            return float(opacity_arg)
        except (TypeError, ValueError):
            return 1.0

    if _is_rgb_sequence(rgb_color_arg):
        return 1.0

    try:
        return float(rgb_color_arg)
    except (TypeError, ValueError):
        return 1.0


def _is_rgb_sequence(value) -> bool:
    """Return True if *value* looks like a length-3 color sequence."""

    if isinstance(value, (str, bytes)):
        return False

    try:
        length = len(value)  # type: ignore[arg-type]
    except TypeError:
        return False

    if length != 3:
        return False

    return True

