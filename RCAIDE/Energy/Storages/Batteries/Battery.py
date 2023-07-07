# RCAIDE/Energy/Storages/Batteries/Battery.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke

""" RCAIDE Package Setup
"""

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

 # RCAIDE imports
from RCAIDE.Core import Data

# Legacy imports 
from Legacy.trunk.S.Components.Energy.Energy_Component import Energy_Component  

# ----------------------------------------------------------------------------------------------------------------------
#  BATTERY
# ----------------------------------------------------------------------------------------------------------------------     
## @ingroup Components-Energy-Storages-Batteries
class Battery(Energy_Component):
    """
    Energy Component object that stores energy. Contains values
    used to indicate its discharge characterics, including a model
    that calculates discharge losses
    """
    def __defaults__(self):
        self.chemistry                      = None 
        self.mass_properties.mass           = 0.0
        self.energy_density                 = 0.0
        self.current_energy                 = 0.0
        self.initial_temperature            = 20.0
        self.current_capacitor_charge       = 0.0
        self.resistance                     = 0.07446 # base internal resistance of battery in ohms  
        self.specific_heat_capacity         = 1100.   
        
        self.pack                           = Data()
        self.pack.max_energy                = 0.0
        self.pack.max_power                 = 0.0
        self.pack.max_voltage               = 0.0 
        
        self.discharge_performance_map      = None  
        self.ragone                         = Data()
        self.ragone.const_1                 = 0.0     # used for ragone functions; 
        self.ragone.const_2                 = 0.0     # specific_power=ragone_const_1*10^(specific_energy*ragone_const_2)
        self.ragone.lower_bound             = 0.0     # lower bound specific energy for which ragone curves no longer make sense
        self.ragone.i                       = 0.0 
