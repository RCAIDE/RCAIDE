# RCAIDE/Library/Compoments/Energy/Fuel_Tanks/Fuel_Tank.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jul 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports
from RCAIDE.Framework.Components import Component

# ----------------------------------------------------------------------------------------------------------------------
#  Fuel Tank
# ----------------------------------------------------------------------------------------------------------------------    
class Fuel_Tank(Component):
    """Fuel tank component class.
    """
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """          
        self.tag                         = 'fuel_tank'
        self.fuel_selector_ratio         = 1.0 
        self.mass_properties.empty_mass  = 0.0   
        self.secondary_fuel_flow         = 0.0
        self.fuel                        = None 