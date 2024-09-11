# RCAIDE/Framework/Components/Airfoil.py
# (c) Copyright 2024 Aerospace Research Community LLC
#
# Created: Sep 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path

# package imports
import numpy as np
from scipy import interpolate

# RCAIDE imports
import RCAIDE.Framework as rcf

# ----------------------------------------------------------------------------------------------------------------------
#  Airfoil
# ----------------------------------------------------------------------------------------------------------------------


@dataclass(kw_only=True)
class Airfoil(rcf.Component):

    thickness_to_chord: float = 0.0
    max_thickness: float = 0.0
    camber: float = 0.0

    coordinates: np.ndarray = field(default_factory=np.empty(shape=(0, 2)))

    x_coordinates: np.ndarray = field(default_factory=np.empty(shape=(0, 1)))
    y_coordinates: np.ndarray = field(default_factory=np.empty(shape=(0, 1)))

    x_upper_surface: np.ndarray = field(default_factory=np.empty(shape=(0, 1)))
    x_lower_surface: np.ndarray = field(default_factory=np.empty(shape=(0, 1)))

    y_upper_surface: np.ndarray = field(default_factory=np.empty(shape=(0, 1)))
    y_lower_surface: np.ndarray = field(default_factory=np.empty(shape=(0, 1)))

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

        x_upper = np.linspace(0, 1, int(np.ceil(n_pts / 2)))
        x_lower = np.linspace(0, 1, int(np.ceil(n_pts / 2)))

        # Concenctrate coordinates near edges

        if edge_factor:
            ef = edge_factor
            x_upper = 1 - (ef + 1) * x_upper * (1 - x_upper) ** ef - (1 - x_upper) ** (ef + 1)
            x_lower = 1 - (ef + 1) * x_lower * (1 - x_lower) ** ef - (1 - x_lower) ** (ef + 1)

        # Compute chordwise thickness distribution
        def _x2t(x):
            return (0.2969 * np.sqrt(x)
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

                idx = np.where(x < camber_location)[0]
                c[idx] = camber / camber_location ** 2 * (2 * camber_location * x[idx] - x[idx] ** 2)

                return c

            c_upper = x2c_corrected(x_upper, c_upper)
            c_lower = x2c_corrected(x_lower, c_lower)

        # Compute surface coordinates

        x_lo    = np.flip(x_lower)
        x_up    = x_upper[1:]
        x       = np.hstack((x_lo, x_up))

        y_lo    = np.flip(c_lower - t_lower)
        y_up    = (c_upper + t_upper)[1:]
        y       = np.hstack((y_lo, y_up))

        return cls(
            name='NACA ' + str(series_number),
            camber=camber,
            max_thickness=thickness,
            thickness_to_chord=thickness / (max(x) - min(x)),
            coordinates=np.vstack((x, y)).T,
            x_coordinates=x,
            y_coordinates=y,
            x_upper_surface=x_up,
            x_lower_surface=x_lo,
            y_upper_surface=y_up,
            y_lower_surface=y_lo
        )

    @classmethod
    def from_file(cls, file_path: str | Path, n_pts: int = 201, interpolation: str = 'cubic'):

        if n_pts % 2 == 0:
            n_pts += 1

        # Open file and read column names and data block
        f = open(file_path, 'r')

        # Extract data
        data_block = f.readlines()
        try:
            # Check for header block
            first_element = float(data_block[0][0])
            if first_element == 1.:
                lednicer_format = False
        except:
            # Check for format line and remove header block
            format_line = data_block[1]

            # Check if it's a Selig or Lednicer file
            try:
                format_flag = float(format_line.strip().split()[0])
            except:
                format_flag = float(format_line.strip().split(',')[0])

            if format_flag > 1.01: # Amount of wiggle room per airfoil tools
                lednicer_format = True
                # Remove header block
                data_block      = data_block[3:]
            else:
                lednicer_format = False
                # Remove header block
                data_block = data_block[1:]

        # Close the file
        f.close()

        if lednicer_format:
            x_up_surf = []
            y_up_surf = []
            x_lo_surf = []
            y_lo_surf = []

            # Loop through each value: append to each column
            upper_surface_flag = True
            for line_count, line in enumerate(data_block):
                #check for blank line which signifies the upper/lower surface division
                line_check = data_block[line_count].strip()
                if line_check == '':
                    upper_surface_flag = False
                    continue
                if upper_surface_flag:
                    x_up_surf.append(float(data_block[line_count].strip().split()[0]))
                    y_up_surf.append(float(data_block[line_count].strip().split()[1]))
                else:
                    x_lo_surf.append(float(data_block[line_count].strip().split()[0]))
                    y_lo_surf.append(float(data_block[line_count].strip().split()[1]))

        else:
            x_up_surf_rev  = []
            y_up_surf_rev  = []
            x_lo_surf      = []
            y_lo_surf      = []

            # Loop through each value: append to each column
            upper_surface_flag = True
            for line_count, line in enumerate(data_block):
                #check for line which starts with 0., which should be the split between upper and lower in selig
                line_check = data_block[line_count].strip()

                # Remove any commas
                line_check = line_check.replace(',','')

                if float(line_check.split()[0]) == 0.:
                    x_up_surf_rev.append(float(data_block[line_count].strip().replace(',','').split()[0]))
                    y_up_surf_rev.append(float(data_block[line_count].strip().replace(',','').split()[1]))

                    x_lo_surf.append(float(data_block[line_count].strip().replace(',','').split()[0]))
                    y_lo_surf.append(float(data_block[line_count].strip().replace(',','').split()[1]))

                    upper_surface_flag = False
                    continue

                if upper_surface_flag:
                    x_up_surf_rev.append(float(data_block[line_count].strip().replace(',','').split()[0]))
                    y_up_surf_rev.append(float(data_block[line_count].strip().replace(',','').split()[1]))
                else:
                    x_lo_surf.append(float(data_block[line_count].strip().replace(',','').split()[0]))
                    y_lo_surf.append(float(data_block[line_count].strip().replace(',','').split()[1]))


                if upper_surface_flag ==True:
                    # check if next line flips without x-coordinate going to 0
                    next_line  = data_block[line_count+1].strip()
                    next_line  = next_line.replace(',','')

                    if next_line.split()[0]>line_check.split()[0] and float(next_line.split()[0]) >0.:
                        upper_surface_flag = False

            # Upper surface values in Selig format are reversed from Lednicer format, so fix that
            x_up_surf_rev.reverse()
            y_up_surf_rev.reverse()

            x_up_surf = x_up_surf_rev
            y_up_surf = y_up_surf_rev

        x_up_surf = np.array(x_up_surf)
        x_lo_surf = np.array(x_lo_surf)
        y_up_surf = np.array(y_up_surf)
        y_lo_surf = np.array(y_lo_surf)

        # Check for extra zeros (OpenVSP exports extra zeros)
        if len(np.unique(x_up_surf))!=len(x_up_surf):
            x_up_surf = x_up_surf[1:]
            x_lo_surf = x_lo_surf[1:]
            y_up_surf = y_up_surf[1:]
            y_lo_surf = y_lo_surf[1:]

        # create custom spacing for more points and leading and trailing edge
        t            = np.linspace(0, 4, n_pts - 1)
        delta        = 0.25
        A            = 5
        f            = 0.25
        smoothsq     = 5 + (2*A/np.pi) *np.arctan(np.sin(2*np.pi*t*f + np.pi/2)/delta)
        dim_spacing  = np.append(0,np.cumsum(smoothsq)/sum(smoothsq))

        # compute thickness, camber and concatenate coodinates
        x_data        = np.hstack((x_lo_surf[::-1], x_up_surf[1:]))
        y_data        = np.hstack((y_lo_surf[::-1], y_up_surf[1:]))
        tck, u        = interpolate.splprep([x_data,y_data], k=3, s=0)
        out           = interpolate.splev(dim_spacing, tck)
        x_data        = out[0]
        y_data        = out[1]

        # shift points to leading edge (x = 0, y = 0)
        x_delta  = min(x_data)
        x_data   = x_data - x_delta

        arg_min  = np.argmin(x_data)
        y_delta  = y_data[arg_min]
        y_data   = y_data - y_delta

        if (x_data[arg_min] == 0) and (y_data[arg_min]  == 0):
            x_data[arg_min]  = 0
            y_data[arg_min]  = 0

        # make sure points start and end at x = 1.0
        x_data[0]  = 1.0
        x_data[-1] = 1.0

        # make sure a small gap at trailing edge
        if (y_data[0] == y_data[-1]):
            y_data[0]          = y_data[0]  - 1E-4
            y_data[-1]         = y_data[-1] + 1E-4

        half_npoints = n_pts//2

        # thickness and camber distributions require equal points
        x_up_surf_old  = np.array(x_up_surf)
        arrx_up_interp = interpolate.interp1d(np.arange(x_up_surf_old.size), x_up_surf_old, kind=interpolation)
        x_up_surf_new  = arrx_up_interp(np.linspace(0, x_up_surf_old.size-1, half_npoints))

        x_lo_surf_old  = np.array(x_lo_surf)
        arrx_lo_interp = interpolate.interp1d(np.arange(x_lo_surf_old.size), x_lo_surf_old, kind=interpolation)
        x_lo_surf_new  = arrx_lo_interp(np.linspace(0, x_lo_surf_old.size-1, half_npoints))

        # y coordinate s
        y_up_surf_old  = np.array(y_up_surf)
        arry_up_interp = interpolate.interp1d(np.arange(y_up_surf_old.size), y_up_surf_old, kind=interpolation)
        y_up_surf_new  = arry_up_interp(np.linspace(0, y_up_surf_old.size-1, half_npoints))

        y_lo_surf_old  = np.array(y_lo_surf)
        arry_lo_interp = interpolate.interp1d(np.arange(y_lo_surf_old.size), y_lo_surf_old, kind=interpolation)
        y_lo_surf_new  = arry_lo_interp(np.linspace(0, y_lo_surf_old.size-1, half_npoints))

        # compute thickness, camber and concatenate coodinates
        thickness      = y_up_surf_new - y_lo_surf_new
        camber         = y_lo_surf_new + thickness/2
        max_t          = np.max(thickness)
        max_c          = max(x_data) - min(x_data)
        t_c            = max_t/max_c

        return cls(
            name=Path(file_path).stem,
            camber=camber,
            max_thickness=max_t,
            thickness_to_chord=t_c,
            coordinates=np.vstack((x_data, y_data)).T,
            x_coordinates=x_data,
            y_coordinates=y_data,
            x_upper_surface=x_up_surf_new,
            x_lower_surface=x_lo_surf_new,
            y_upper_surface=y_up_surf_new,
            y_lower_surface=y_lo_surf_new
        )