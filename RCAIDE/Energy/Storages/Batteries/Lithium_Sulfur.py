# RCAIDE/Energy/Storages/Batteries/Lithium_Sulfur.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports
import RCAIDE

# package imports
from RCAIDE.Core import Units
from . import Battery

# ----------------------------------------------------------------------------------------------------------------------
#  BATTERY
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Energy-Storages-Batteries 
class Lithium_Sulfur(Battery):
    """
    Specifies discharge/specific energy characteristics specific to
    lithium-ion batteries
    """
    
    def __defaults__(self):
        self.specific_energy    = 500     *Units.Wh/Units.kg
        self.specific_power     = 1       *Units.kW/Units.kg
        self.ragone.const_1     = 245.848 *Units.kW/Units.kg
        self.ragone.const_2     = -.00478 /(Units.Wh/Units.kg)
        self.ragone.lower_bound = 300     *Units.Wh/Units.kg
        self.ragone.upper_bound = 700     *Units.Wh/Units.kg