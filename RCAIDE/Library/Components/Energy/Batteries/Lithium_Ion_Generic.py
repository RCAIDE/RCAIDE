## @ingroup Library-Compoments-Energy-Batteries
# RCAIDE/Library/Compoments/Energy/Sources/Batteries/Lithium_Ion.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Mar 2024, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

 # RCAIDE imports
from .Battery import Battery  
from RCAIDE.Framework.Core                      import Units, Data
from RCAIDE.Library.Methods.Energy.Sources.Battery.Lithium_Ion_Generic  import compute_generic_li_cell_performance 

# ----------------------------------------------------------------------
#  Lithium_Ion_Generic
# ----------------------------------------------------------------------    
## @ingroup Library-Compoments-Energy-Batteries 
class Lithium_Ion_Generic(Battery):
    """ Generic lithium ion battery.  
    """  
    def __defaults__(self):
        """This sets the default values.
    
        Assumptions:
          Default discharge curves correspond to lithium-iron-phosphate cells 
          Convective Thermal Conductivity Coefficient corresponds to forced  air cooling in 35 m/s air  

        Source:
            None
        """    
        self.tag                                                      = 'lithium_ion_generic'  
        self.cell                                                     = Data()  
        self.pack                                                     = Data()
        self.module                                                   = Data()  
        self.bus_power_split_ratio                                    = 1.0
        
        self.age                                                      = 0       # [days]
        self.cell.mass                                                = 0.03  * Units.kg  
        self.cell.charging_current                                    = 1.0     # [Amps]
        self.cell.charging_voltage                                    = 3       # [Volts]
        self.cell.specific_heat_capacity                              = 1115    # [J/kgK] 
        self.cell.maximum_voltage                                     = 3.6     # [V]   
        self.cell.specific_energy                                     = 200.    *Units.Wh/Units.kg    
        self.cell.specific_power                                      = 1.      *Units.kW/Units.kg
                                     
        self.convective_heat_transfer_coefficient                     = 35.     # [W/m^2K] 
        self.heat_transfer_efficiency                                 = 1.0       
                    
        self.pack.electrical_configuration                            = Data()
        self.pack.electrical_configuration.series                     = 1
        self.pack.electrical_configuration.parallel                   = 1  
        self.pack.electrical_configuration.total                      = 1   
        self.pack.number_of_modules                                   = 1
         
        self.module.number_of_cells                                   = 1                   
        self.module.electrical_configuration                          = Data()
        self.module.electrical_configuration.series                   = 1
        self.module.electrical_configuration.parallel                 = 1   
        self.module.electrical_configuration.total                    = 1   
        self.module.geometrtic_configuration                          = Data() 
        self.module.geometrtic_configuration.normal_count             = 1       # number of cells normal to flow
        self.module.geometrtic_configuration.parallel_count           = 1       # number of cells parallel to flow      
        self.module.geometrtic_configuration.normal_spacing           = 0.02
        self.module.geometrtic_configuration.parallel_spacing         = 0.02 
        
        # defaults that are overwritten if specific cell chemistry is used 
        self.ragone.const_1                                           = 88.818  *Units.kW/Units.kg
        self.ragone.const_2                                           = -.01533 /(Units.Wh/Units.kg)
        self.ragone.lower_bound                                       = 60.     *Units.Wh/Units.kg
        self.ragone.upper_bound                                       = 225.    *Units.Wh/Units.kg    
        return           


    def energy_calc(self,state,bus,discharge= True): 
        """Computes the state of a generic battery cell.
           
        Assumptions:
            Assumes the discharge profile of LFP cell
            
        Source:
            None
    
        Args:
            self         (dict): battery        [-]
            state        (dict): temperature    [K]
            bus          (dict): electric bus   [-]
            discharge (boolean): discharge flag [-]
            
        Returns: 
            None
        """     
        compute_generic_li_cell_performance(self,state,bus,discharge) 
                        
        return       
    
    def compute_voltage(self,battery_conditions):
        """ Computes the voltage of a single cell    
    
        Assumptions:
            Properties of the LFP cell is used 
        
        Source:
            None
    
        Args:
            self               (dict): battery          [-] 
            battery_conditions (dict): state of battery [-]
            
        Returns: 
            None
        """      
        return battery_conditions.pack.voltage_under_load 
 
 
  