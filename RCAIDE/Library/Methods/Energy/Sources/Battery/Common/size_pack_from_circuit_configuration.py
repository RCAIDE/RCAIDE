## @ingroup Library-Methods-Energy-Sources-Battery-Common
# RCAIDE/Library/Methods/Energy/Sources/Battery/Common/size_pack_from_circuit_configuration.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
# size_pack_from_circuit_configuration
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Energy-Sources-Battery-Common
def size_pack_from_circuit_configuration(battery,module_weight_factor = 1.42):  
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

    Args:
       battery              (dict): battery data structure [-] 
       pack_markup_factor (float): pack mark up factor     [unitless]
                          
    Returns:
       None 
    """     
    cumulative_battery_cell_mass                = battery.cell.mass * battery.pack.electrical_configuration.series * battery.pack.electrical_configuration.parallel   
 
    battery.pack.maximum_energy                 = cumulative_battery_cell_mass * battery.cell.specific_energy    
    battery.pack.maximum_power                  = cumulative_battery_cell_mass * battery.cell.specific_power 
    battery.pack.maximum_voltage                = battery.cell.maximum_voltage  * battery.pack.electrical_configuration.series   
    battery.pack.initial_maximum_energy         = battery.pack.maximum_energy
    
    battery.mass_properties.mass                = cumulative_battery_cell_mass*module_weight_factor 
    battery.pack.specific_energy                = battery.pack.maximum_energy / battery.mass_properties.mass
    battery.pack.specific_power                 = battery.pack.maximum_power / battery.mass_properties.mass
    battery.pack.electrical_configuration.total = battery.pack.electrical_configuration.series * battery.pack.electrical_configuration.parallel
    
    # charging properties 
    battery.pack.charging_voltage               = battery.cell.charging_voltage * battery.pack.electrical_configuration.series     
    battery.pack.charging_current               = battery.cell.charging_current * battery.pack.electrical_configuration.parallel      
    
    return 
