## @ingroup Methods-Energy-Sources-Battery-Common
# RCAIDE/Methods/Energy/Sources/Battery/Common/initialize_from_circuit_configuration.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

from RCAIDE.Framework.Core import Units 

# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Sources-Battery-Common
def initialize_from_circuit_configuration(battery,module_weight_factor = 1.42):  
    """Calculate pack level properties of battery using cell 
    properties and module configuraton
    
    Assumptions:
    Total battery pack mass contains build-up factor (1.42) for battery casing,
    internal wires, thermal management system and battery management system 
    Factor computed using information of battery properties for X-57 Maxwell 
    Aircraft
    
    Source:
    Cell Charge: Chin, J. C., Schnulo, S. L., Miller, T. B., Prokopius, K., and Gray, 
    J., Battery Performance Modeling on Maxwell X-57",AIAA Scitech, San Diego, CA,
    2019. URLhttp://openmdao.org/pubs/chin_battery_performance_x57_2019.pdf.     

    Inputs:
    mass              
    battery.cell
      nominal_capacity        [amp-hours]            
      nominal_voltage         [volts]
      pack_config             [unitless]
      mass                    [kilograms]
                          
    Outputs:              
     battery.             
       maximum_energy         [watt-hours]
       maximum_power              [watts]
       initial_maximum_energy [watt-hours]
       specific_energy        [watt-hours/kilogram]
       charging_voltage       [volts]
       charging_current       [amps]
       mass_properties.    
        mass                  [kilograms] 
    """    
    amp_hour_rating                             = battery.cell.nominal_capacity    
    nominal_voltage                             = battery.cell.nominal_voltage       
    total_battery_assemply_mass                 = battery.cell.mass * battery.pack.electrical_configuration.series * battery.pack.electrical_configuration.parallel   
    battery.mass_properties.mass                = total_battery_assemply_mass*module_weight_factor  
    battery.specific_energy                     = (amp_hour_rating*nominal_voltage)/battery.cell.mass  * Units.Wh/Units.kg   
    battery.pack.maximum_energy                 = total_battery_assemply_mass*battery.specific_energy    
    battery.specific_power                      = battery.specific_energy/battery.cell.nominal_capacity 
    battery.pack.maximum_power                  = battery.specific_power*battery.mass_properties.mass  
    battery.pack.maximum_voltage                = battery.cell.maximum_voltage  * battery.pack.electrical_configuration.series   
    battery.pack.initial_maximum_energy         = battery.pack.maximum_energy      
    battery.charging_voltage                    = battery.cell.charging_voltage * battery.pack.electrical_configuration.series     
    battery.charging_current                    = battery.cell.charging_current * battery.pack.electrical_configuration.parallel  
    battery.pack.electrical_configuration.total = battery.pack.electrical_configuration.series * battery.pack.electrical_configuration.parallel        
