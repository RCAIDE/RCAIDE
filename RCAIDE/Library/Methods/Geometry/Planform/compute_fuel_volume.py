# RCAIDE/Library/Methods/Geometry/Planform/compute_fuel_volume.py
# 
# 
# Created:  Jul 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
import RCAIDE 
from RCAIDE.Library.Methods.Geometry.Airfoil import import_airfoil_geometry,  compute_naca_4series  
from RCAIDE.Library.Methods.Geometry.Planform.convert_sweep import convert_sweep_segments 
from RCAIDE.Framework.Core import Units
import matplotlib.pyplot as plt

# python imports 
import numpy as np   
from scipy.interpolate import interp1d
from shapely.geometry import Polygon, Point
from copy import  deepcopy
import os 

# ----------------------------------------------------------------------------------------------------------------------
# compute_fuel_volume 
# ----------------------------------------------------------------------------------------------------------------------
def compute_fuel_volume(vehicle, update_max_fuel =True):
    wings     = vehicle.wings
    fuselages = vehicle.fuselages
    total_fuel_volume = 0
    total_fuel_mass   = 0
    
    for network in vehicle.networks: 
        for fuel_line in network.fuel_lines:
            for fuel_tank in fuel_line.fuel_tanks: 
                fuel_tank.internal_volume = 0
                volume = fuel_tank.compute_volume(wings,fuselages)
                total_fuel_volume     += volume
                total_fuel_mass       +=fuel_tank.mass_properties.fuel
    vehicle.total_fuel_volume = total_fuel_volume
