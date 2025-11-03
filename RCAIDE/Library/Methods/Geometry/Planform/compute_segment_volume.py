# RCAIDE/Library/Methods/Geometry/Planform/compute_segment_volume.py
# 
# 
# Created:  Jul 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
from copy import deepcopy
import RCAIDE
from RCAIDE.Library.Methods.Geometry.Airfoil import compute_naca_4series

import numpy as np
from scipy.interpolate import interp1d


def compute_segment_volume(wing, inner_segment, outer_segment, n_points=401, n_span=51):

    # Extract airfoil coordinates
    if hasattr(inner_segment.airfoil,'geometry') is False or hasattr(outer_segment.airfoil,'geometry') is False: # first, if airfoil geometry data not defined, import from geoemtry files
        inner_segment = deepcopy(inner_segment)
        outer_segment = deepcopy(outer_segment)
        if type(inner_segment.airfoil) == RCAIDE.Library.Components.Airfoils.NACA_4_Series_Airfoil: # check if naca 4 series of airfoil from datafile
            try:
                inner_segment.airfoil.geometry = compute_naca_4series(inner_segment.NACA_4_Series_code,n_points)
            except:
                inner_segment.airfoil.geometry = compute_naca_4series('0012')
        else:
            inner_segment.airfoil= RCAIDE.Library.Components.Airfoils.NACA_4_Series_Airfoil
            inner_segment.airfoil.geometry = compute_naca_4series('0012')
        
        if type(outer_segment.airfoil) == RCAIDE.Library.Components.Airfoils.NACA_4_Series_Airfoil: # check if naca 4 series of airfoil from datafile
            try:
                outer_segment.airfoil.geometry = compute_naca_4series(outer_segment.NACA_4_Series_code,n_points)
            except:
                outer_segment.airfoil.geometry = compute_naca_4series('0012')
        else:
            outer_segment.airfoil= RCAIDE.Library.Components.Airfoils.NACA_4_Series_Airfoil
            outer_segment.airfoil.geometry = compute_naca_4series('0012')
    
      
    x_in = np.array(inner_segment.airfoil.geometry.x_coordinates)
    y_in = np.array(inner_segment.airfoil.geometry.y_coordinates)
    x_out = np.array(outer_segment.airfoil.geometry.x_coordinates)
    y_out = np.array(outer_segment.airfoil.geometry.y_coordinates)

    x_in, idx = np.unique(x_in, return_index=True)
    y_in = y_in[idx]

    x_out, idx = np.unique(x_out, return_index=True)
    y_out = y_out[idx]

    # Compute segment span length
    L = (outer_segment.percent_span_location - inner_segment.percent_span_location) * wing.spans.projected

    # Resample both airfoils to common cosine x-grid
    beta = np.linspace(0, np.pi, n_points)
    x_common = 0.5 * (1 - np.cos(beta))

    f_in = interp1d(x_in, y_in, kind='cubic', fill_value="extrapolate")
    f_out = interp1d(x_out, y_out, kind='cubic', fill_value="extrapolate")

    y_in_resampled = f_in(x_common)
    y_out_resampled = f_out(x_common)

    A_in = polygon_area(x_common, y_in_resampled)
    A_out = polygon_area(x_common, y_out_resampled)

    # Interpolate between the two sections spanwise
    t = np.linspace(0, 1, n_span)
    areas = (1 - t) * A_in + t * A_out

    # Integrate area along span to get volume
    volume = np.trapezoid(areas, t) * L  # m³ if inputs are in meters

    return volume

# Compute areas of each section (shoelace formula)
def polygon_area(x, y):
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))