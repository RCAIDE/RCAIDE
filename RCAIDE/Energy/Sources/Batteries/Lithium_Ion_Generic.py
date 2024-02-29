## @ingroup Energy-Sources-Batteries
# RCAIDE/Energy/Sources/Batteries/Lithium_Ion.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

 # RCAIDE imports
from RCAIDE.Core                      import Units, Data 
from RCAIDE.Energy.Sources.Batteries  import Battery  
from RCAIDE.Methods.Energy.Sources.Battery.Lithium_Ion_Generic  import compute_generic_li_cell_performance 

# ----------------------------------------------------------------------
#  Lithium_Ion_Generic
# ----------------------------------------------------------------------    
## @ingroup Energy-Sources-Batteries 
class Lithium_Ion_Generic(Battery):
    """ Generic lithium ion battery that specifies discharge/specific energy 
    characteristics. 
    
    Assumptions
    1) Default discharge curves correspond to lithium-iron-phosphate cells
    
    2) Convective Thermal Conductivity Coefficient corresponds to forced
    air cooling in 35 m/s air 
    
    Inputs:
    None
    
    Outputs:
    None
    
    Properties Used:
    N/A
    """  
    def __defaults__(self):
            
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
        self.specific_energy                                          = 200.    *Units.Wh/Units.kg    
        self.specific_power                                           = 1.      *Units.kW/Units.kg
        self.ragone.const_1                                           = 88.818  *Units.kW/Units.kg
        self.ragone.const_2                                           = -.01533 /(Units.Wh/Units.kg)
        self.ragone.lower_bound                                       = 60.     *Units.Wh/Units.kg
        self.ragone.upper_bound                                       = 225.    *Units.Wh/Units.kg    
        return           


    def energy_calc(self,state,bus,battery_discharge_flag= True): 
        """This is an electric cycle model for 18650 lithium-iron_phosphate battery cells. It
           models losses based on an empirical correlation Based on method taken 
           from Datta and Johnson.
           
           Assumptions:  
           
           Inputs: 
           
           Outputs: 
            
        """  
        compute_generic_li_cell_performance(self,state,bus,battery_discharge_flag) 
                        
        return       
    
    def compute_voltage(self,battery_conditions):
        """ Computes the voltage of a single LFP cell or a battery pack of LFP cells   
    
            Assumptions:
            None
    
            Source:
            N/A
    
            Inputs:  
                state   - segment unknowns to define voltage [unitless]
            
            Outputs
                V_ul    - under-load voltage                 [volts]
             
            Properties Used:
            N/A
        """              

        return battery_conditions.pack.voltage_under_load 
    
    def update_battery_age(self,segment,increment_battery_age_by_one_day = False):   
        pass 
        return  
 
 
  