## @ingroup Compoments-Energy-Fuel_Tanks 
# RCAIDE/Energy/Sources/Fuel_Tanks/Fuel_Tanks.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from RCAIDE.Components    import Component   

# ----------------------------------------------------------------------------------------------------------------------
#  Fuel Tank
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Compoments-Energy-Fuel_Tanks 
class Fuel_Tank(Component):
    """
    Energy Component object that stores fuel. Contains values
    used to indicate its fuel type.
    """
    def __defaults__(self):
        self.tag                         = 'fuel_tank'
        self.fuel_selector_ratio         = 1.0 
        self.mass_properties.empty_mass  = 0.0   
        self.secondary_fuel_flow         = 0.0
        self.fuel                        = None 