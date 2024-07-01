## @ingroup Library-Compoments-Energy-Batteries
# RCAIDE/Library/Compoments/Energy/Sources/Batteries/Lithium_Sulfur.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# package imports
from RCAIDE.Framework.Core import Units
from . import Battery

# ----------------------------------------------------------------------------------------------------------------------
#  Lithium_Sulfur
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Compoments-Energy-Batteries 
class Lithium_Sulfur(Battery):
    """Lithium-Sulphur battery.
    """ 
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """   
        self.cell.specific_energy    = 500     *Units.Wh/Units.kg
        self.cell.specific_power     = 1       *Units.kW/Units.kg
        self.power.specific_energy   = 500     *Units.Wh/Units.kg
        self.power.specific_power    = 1       *Units.kW/Units.kg
        self.ragone.const_1          = 245.848 *Units.kW/Units.kg
        self.ragone.const_2          = -.00478 /(Units.Wh/Units.kg)
        self.ragone.lower_bound      = 300     *Units.Wh/Units.kg
        self.ragone.upper_bound      = 700     *Units.Wh/Units.kg