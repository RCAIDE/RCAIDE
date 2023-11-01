## @ingroup Components-Airfoils
# Airfoil.py
# 
# Created:  Oct 2023, Racheal M. Erhard
# Modified: 


# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
from Legacy.trunk.S.Core import Data
from Legacy.trunk.S.Components import Lofted_Body

import Aircraft_Modules
import os
# ------------------------------------------------------------
#   Airfoil
# ------------------------------------------------------------

## @ingroup Components-Airfoils
class Airfoil(Lofted_Body.Section):
    def __defaults__(self):
        """This sets the default values of a airfoil defined in SUAVE.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """         
        
        self.tag                        = 'Airfoil' 
        self.airfoil_directory          = None
        self.coordinate_file            = None

        self.settings = Data()
        self.settings.number_of_points = 200
        self.settings.NACA_4_series_flag = False
        self.settings.NACA_4_series_digits = '4412'
        self.settings.leading_and_trailing_edge_resolution_factor = 1.5
        self.settings.surface_interpolation = "cubic"  # type of interpolation used in the SciPy function. Preferable options are linear, quardratic and cubic. 
                                                       # Full list of options can be found here : https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.interp1d.html#scipy.interpolate.interp1d

        self.geometry                   = Data()
        self.geometry.thickness_to_chord = None
        self.geometry.max_thickness      = None
        self.geometry.x_coordinates      = None
        self.geometry.y_coordinates      = None
        self.geometry.x_upper_surface    = None
        self.geometry.x_lower_surface    = None
        self.geometry.y_upper_surface    = None
        self.geometry.y_lower_surface    = None
        self.geometry.camber_coordinates = None
        
        
    def initialize(self):
        """
        Initialize this airfoil.
        """
        # Default airfoil directory used if unspecified
        if self.airfoil_directory is None:
            self.airfoil_directory = f"{os.path.dirname(Aircraft_Modules.__file__)}/Airfoils/Clark_y" 
            print(f'Warning: No airfoil directory specified. Defaulted to: {self.airfoil_directory}')
        
        # Default airfoil coordinate file path, relative to airfoil_directory
        if self.coordinate_file is None and not self.settings.NACA_4_series_flag:
            self.coordinate_file = 'Clark_Y.txt'
            print(f'Warning: No airfoil coordinate file specified. Defaulted to: {self.coordinate_file}')
        
        return