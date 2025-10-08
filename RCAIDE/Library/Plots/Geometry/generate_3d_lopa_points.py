# RCAIDE/Library/Plots/Geometry/generate_3d_lopa_points.py
#
# Created: Oct 2025, S Shekar 

import numpy as np
import vtk
import matplotlib.colors as mcolors
from RCAIDE.Framework.Core import Data

# --- CONSTANTS ---
DEFAULT_SEAT_HEIGHT = 0.45
DEFAULT_SEAT_CLEARANCE = 0.05
SEAT_LENGTH_SCALE = 0.90
SEAT_WIDTH_SCALE = 0.90
MIN_DIMENSION = 1e-3

BUSINESS_COLOR = mcolors.to_rgb("seagreen")
ECONOMY_COLOR = mcolors.to_rgb("steelblue")


def generate_3d_lopa_points(structure):
    """Generate VTK seat geometry for Layout Of Passenger Accommodation (LOPA)."""

    layout = getattr(structure, "layout_of_passenger_accommodations", None)
    if layout is None or not hasattr(layout, "object_coordinates"):
        return _empty_geometry()

    coords = np.asarray(layout.object_coordinates, float)

    seats = []
    business_count = 0
    economy_count = 0
    seat_height = getattr(structure, "seat_height", DEFAULT_SEAT_HEIGHT) or DEFAULT_SEAT_HEIGHT

    for row in coords:
        # columns: 8=business flag, 9=economy flag, 2=x, 3=y, 4=z, 5=length, 6=width
        if row[8] == 1.0:
            seat_class = "business"
            business_count += 1
        elif row[9] == 1.0:
            seat_class = "economy"
            economy_count += 1
        else:
            continue

        x, y, z = row[2], row[3], row[4] + DEFAULT_SEAT_CLEARANCE
        length = max(abs(row[5]) * SEAT_LENGTH_SCALE, MIN_DIMENSION)
        width = max(abs(row[6]) * SEAT_WIDTH_SCALE, MIN_DIMENSION)

        cube = vtk.vtkCubeSource()
        cube.SetCenter(x, y, z + 0.5 * seat_height)
        cube.SetXLength(length)
        cube.SetYLength(width)
        cube.SetZLength(seat_height)
        cube.Update()

        polydata = vtk.vtkPolyData()
        polydata.ShallowCopy(cube.GetOutput())

        seats.append({"polydata": polydata, "class": seat_class})

    geom = _empty_geometry()
    geom._lopa_seats = seats
    geom.metadata = Data()
    geom.metadata.business_seat_count = business_count
    geom.metadata.economy_seat_count = economy_count
    return geom


def _empty_geometry():
    geom = Data()
    geom.PTS = np.zeros((1, 1, 3))
    geom._lopa_seats = []
    geom.metadata = Data()
    geom.metadata.business_seat_count = 0
    geom.metadata.economy_seat_count = 0
    return geom
