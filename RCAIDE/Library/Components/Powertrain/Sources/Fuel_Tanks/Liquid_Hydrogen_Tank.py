# RCAIDE/Library/Components/Powertrain/Energy/Sources/Fuel_Tanks/Non_Integral_Tank.py
# 
# 
# Created:  September 2024, A. Molloy and M. Clarke 
# Modified: Aug 2025, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
import RCAIDE
from .Non_Integral_Tank  import Non_Integral_Tank 
from RCAIDE.Library.Methods.Powertrain.Sources.Fuel_Tanks.Non_Integral_Tank.compute_non_integral_tank_volume import *
from RCAIDE.Library.Methods.Powertrain.Sources.Fuel_Tanks.Liquid_Hydrogen_Tank.compute_structural_performance import structural_solver

# ----------------------------------------------------------------------------------------------------------------------
#  Fuel Tank
# ---------------------------------------------------------------------------------------------------------------------    
class Liquid_Hydrogen_Tank(Non_Integral_Tank):
    """
    A class representing a liquid hydrogen tank.
    """
    def __defaults__(self):
        self.tag = 'Liquid_Hydrogen_Tank'
        self.material   = None
        self.insulation_material = None
        self.design_inlet_temperature= 15
        self.design_altitiude = 0
        self.acceptable_heat_leak = 20
        self.ullage_volume_fraction = 0.07 # Volume fraction
        self.aspect_ratio = self.length/self.outer_diameter


    def compute_volume(self,wings,fuselages):
        if self.wing_tag != None:
                wing = wings[self.wing_tag]  
                _ = compute_wing_non_integral_tank_volume(self,wing)
                structural_solver(self)

        elif self.fuselage_tag != None: 
            fuselage = fuselages[self.fuselage_tag]  
            volume = compute_fuselage_non_integral_tank_fuel_volume(self,fuselage)
        else:
            if self.bwb_aft_tank == True:
                wing = wings[self.wing_root_tag]  
                volume = compute_bwb_aft_tank_volume(self,wing)
        return  volume

        


