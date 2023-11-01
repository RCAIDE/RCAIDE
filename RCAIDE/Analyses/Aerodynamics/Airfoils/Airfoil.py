## @ingroup Analyses-Aerodynamics-Airfoils
# Airfoil.py
#
# Created:  Oct 2023, Racheal M. Erhard
# Modified: 

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
# Legacy imports
from Legacy.trunk.S.Core import Data, Units
from Legacy.trunk.S.Analyses import Analysis

# RCAIDE imports
from RCAIDE.Methods.Aerodynamics.Airfoil.import_airfoil_geometry import import_airfoil_geometry
from RCAIDE.Methods.Aerodynamics.Airfoil.compute_naca_4series_geometry import compute_naca_4series_geometry
from RCAIDE.Methods.Aerodynamics.Airfoil.compute_airfoil_properties_from_polar_files import compute_airfoil_properties_from_polar_files
from RCAIDE.Methods.Aerodynamics.Airfoil.compute_airfoil_properties_from_panel_method import compute_airfoil_properties_from_panel_method

# External package imports
import numpy as np


# ----------------------------------------------------------------------
#  Analysis
# ----------------------------------------------------------------------
## @ingroup Analyses-Aerodynamics-Airfoils
class Airfoil(Analysis):
    """This is the class for airfoil analyses. It contains functions
    for airfoil analysis.
    
    Assumptions:
    None
    
    Source:
    N/A
    """
    def __defaults__(self):
        """This sets the default values and methods for the airfoil analysis.

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
        self.tag = 'Airfoil_Analysis'
        self.geometry = Data() # Vehicle data structure, used to extract airfoil components
        
        self.airfoil_data = Data() # Data structure that will contain data from all airfoils in analysis
        
        self.settings = Data()
        self.settings.use_pre_stall_data = True
        
        # Settings for panel method
        self.settings.use_panel_method = False      
        self.settings.panel_method = Data()
        self.settings.panel_method.angle_of_attack_range = np.array([-4, 0, 2, 4, 8, 10, 14]) * Units.degrees 
        self.settings.panel_method.Reynolds_number_range = np.array([1, 5, 10, 30, 50, 75, 100]) * 1E4  
        self.settings.panel_method.initial_momentum_thickness = 1E-5
        self.settings.panel_method.tolerance = 1
        self.settings.panel_method.H_wake = 1.05
        self.settings.panel_method.Ue_wake = 0.99
        
        # Settings for polar import method
        self.settings.use_polar_import = True      
        self.settings.polar_import_method = Data()  
        self.settings.polar_import_method.polar_files = None 
        self.settings.polar_import_method.interpolated_angle_of_attack_lower_bound = -6
        self.settings.polar_import_method.interpolated_angle_of_attack_upper_bound = 16
        self.settings.polar_import_method.angle_of_attack_discretization = 89 # Number of angles of attack over which to interpolate from the direct data. 
                                    # This is required if more than one polar file is analyzed, as the output structure is assumed to have the same shape.
        
        
        
    def initialize(self):
        """
        Initializes the airfoil with a default geometry file and polar data files unless otherwise provided.
        Checks for all airfoils attached to any wing or rotor components in the geoemtry.
        
        Assumptions:
        None
        
        Source:
        N/A
        
        Inputs:
        None
        
        Outputs:
        None
        
        """
        
        # Initialize the analysis with the proper evaluate method
        if self.settings.use_panel_method:
            self.evaluate = self.evaluate_with_panel_method
        elif self.settings.use_polar_import:
            self.evaluate = self.evaluate_with_polar_files
        else:
            self.evaluate = None
        return
        
        
    def evaluate_with_polar_files(self):
        """Evaluates all airfoils in the specified vehicle geometry. 
        Wing airfoils only require geometry import. Rotor airfoils require
        both geometry import and polar data calculation. Polar data calculation
        is performed using provided polar data files combined with post-stall
        models.

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
        geometry = self.geometry
        if bool(geometry.Airfoil_Components):
            for airfoil in geometry.Airfoil_Components:
                # Initialize airfoil
                airfoil.initialize()
                
                # Evaluate airfoil geometry for this rotor
                if airfoil.settings.NACA_4_series_flag:
                    airfoil.geometry = compute_naca_4series_geometry(airfoil)
                else:
                    airfoil.geometry = import_airfoil_geometry(airfoil)
                
                # Compute airfoil polar surrogate using provided polar files, append as analysis polars
                self.airfoil_data[airfoil.tag] = compute_airfoil_properties_from_polar_files(self, airfoil)
        else:
            raise Exception("No Airfoil_Components in specified geometry! Required for airfoil polar evaluation.")
                
        return
    
    def evaluate_with_panel_method(self):
        """Evaluates all airfoils in the specified vehicle geometry. 
        Wing airfoils only require geometry import. Rotor airfoils require
        both geometry import and polar data calculation. 
        
        Polar data calculation is performed using the panel method combined with 
        post-stall model.

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
        geometry = self.geometry
        if bool(geometry.Airfoil_Components):
            for airfoil in geometry.Airfoil_Components:
                # Initialize airfoil
                airfoil.initialize()
                
                # Evaluate airfoil geometry for this rotor
                if airfoil.settings.NACA_4_series_flag:
                    airfoil.geometry = compute_naca_4series_geometry(airfoil)
                else:
                    airfoil.geometry = import_airfoil_geometry(airfoil)
                
                # Compute airfoil polar surrogate using provided polar files, append as analysis polars
                self.airfoil_data[airfoil.tag] = compute_airfoil_properties_from_panel_method(self, airfoil)
        else:
            raise Exception("No Airfoil_Components in specified geometry! Required for airfoil polar evaluation.")
        
        return
