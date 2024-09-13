## @ingroup Library-Compoments-Energy-Batteries
# RCAIDE/Library/Compoments/Energy/Sources/Batteries/Battery.py
# 
# 
# Created:  Mar 2024, M. Clarke
# Modified: Sep 2024, S. Shekar
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports
from RCAIDE.Framework.Core        import Data
from RCAIDE.Library.Components    import Component   
from RCAIDE.Library.Methods.Energy.Sources.Batteries.Common.append_battery_conditions import append_battery_conditions, append_battery_segment_conditions

# ----------------------------------------------------------------------------------------------------------------------
#  Battery
# ----------------------------------------------------------------------------------------------------------------------     
## @ingroup Library-Components-Energy-Batteries
class Battery(Component):
    """Default battery class."""
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
            None
        
        Source:
            None
        """      
        self.chemistry                                         = None 
        self.assigned_propulsors                               = None
        self.mass_properties.mass                              = 0.0
        self.energy_density                                    = 0.0
        self.current_energy                                    = 0.0
        self.initial_temperature                               = 20.0
        self.current_capacitor_charge                          = 0.0
        self.resistance                                        = 0.07446 # base internal resistance of battery in ohms  
        self.specific_heat_capacity                            = 1100.   
                            
        self.pack                                              = Data()
        self.pack.maximum_energy                               = 0.0
        self.pack.maximum_power                                = 0.0
        self.pack.maximum_voltage                              = 0.0 
                            
        self.discharge_performance_map                         = None  
        self.ragone                                            = Data()
        self.ragone.const_1                                    = 0.0     # used for ragone functions; 
        self.ragone.const_2                                    = 0.0     # specific_power=ragone_const_1*10^(specific_energy*ragone_const_2)
        self.ragone.lower_bound                                = 0.0     # lower bound specific energy for which ragone curves no longer make sense
        self.ragone.i                                          = 0.0 
                      
        self.thermal_management_system                         = Data()    
        
         
    def append_operating_conditions(self,segment,bus):  
        append_battery_conditions(self,segment,bus)  
        return
    
    
    def append_battery_segment_conditions(self,bus, conditions, segment):
        append_battery_segment_conditions(self,bus, conditions, segment)
        return

 