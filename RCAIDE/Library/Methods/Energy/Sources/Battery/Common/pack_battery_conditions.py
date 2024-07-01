## @ingroup Library-Methods-Energy-Sources-Battery 
# RCAIDE/Library/Methods/Energy/Sources/Battery/Common/pack_battery_conditions.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  pack_battery_conditions
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Energy-Sources-Battery 
def pack_battery_conditions(battery_conditions,battery): 
    """ Packs the results from the network into propulsion data structures.
    
        Assumptions:
           None
    
        Source:
           None 
    
        Args:
        battery_conditions  (dict): operating conditions of battery [-]
        battery.
               inputs.current                (numpy.ndarray): [Amperes]
               inputs.power                  (numpy.ndarray): [Watts]
               current_energy                (numpy.ndarray): [Joules]
               voltage_open_circuit          (numpy.ndarray): [Volts]
               voltage_under_load            (numpy.ndarray): [Volts] 
               maximum_energy                (numpy.ndarray): [Joules]
               age                                     (int): [days]
               mass_properties.mass                  (float): [kilograms] 
               internal_resistance           (numpy.ndarray): [Ohms]
               state_of_charge               (numpy.ndarray): [unitless]
               pack.temperature              (numpy.ndarray): [Kelvin]
               heat_energy_generated         (numpy.ndarray): [Joules]
               cell.charge_throughput        (numpy.ndarray): [Ampere-hours]
               cell.voltage_under_load       (numpy.ndarray): [Volts]  
               cell.voltage_open_circuit     (numpy.ndarray): [Volts]  
               cell.current                  (numpy.ndarray): [Amperes]
               cell.temperature              (numpy.ndarray): [Kelvin] 
               cell.joule_heat_fraction      (numpy.ndarray): [unitless]  
               cell.entropy_heat_fraction    (numpy.ndarray): [unitless] 
               
        Returns:
           None 
    """      
    n_series           = battery.pack.electrical_configuration.series  
    n_parallel         = battery.pack.electrical_configuration.parallel
    n_total            = n_series*n_parallel 
    battery_power_draw = battery.outputs.power    
        
    battery_conditions.pack.current                         = battery.outputs.current
    battery_conditions.pack.energy                          = battery.pack.current_energy
    battery_conditions.pack.voltage_open_circuit            = battery.pack.voltage_open_circuit
    battery_conditions.pack.voltage_under_load              = battery.pack.voltage_under_load 
    battery_conditions.pack.power_draw                      = battery_power_draw   
    battery_conditions.pack.temperature                     = battery.pack.temperature  
    battery_conditions.pack.heat_energy_generated           = battery.pack.heat_energy_generated
    battery_conditions.pack.efficiency                      = (battery_power_draw+battery.pack.heat_energy_generated)/battery_power_draw          
    battery_conditions.pack.specfic_power                   = -battery_power_draw/battery.mass_properties.mass   
    battery_conditions.pack.internal_resistance             = battery.pack.internal_resistance 
    battery_conditions.cell.cycle_in_day                    = battery.cell.age
    battery_conditions.cell.state_of_charge                 = battery.cell.state_of_charge 
    battery_conditions.cell.power                           = battery.outputs.power/n_series
    battery_conditions.cell.energy                          = battery.pack.current_energy/n_total   
    battery_conditions.cell.voltage_under_load              = battery.cell.voltage_under_load    
    battery_conditions.cell.voltage_open_circuit            = battery.cell.voltage_open_circuit  
    battery_conditions.cell.current                         = abs(battery.cell.current)        
    battery_conditions.cell.temperature                     = battery.cell.temperature
    battery_conditions.cell.charge_throughput               = battery.cell.charge_throughput
    battery_conditions.cell.joule_heat_fraction             = battery.cell.joule_heat_fraction   
    battery_conditions.cell.entropy_heat_fraction           = battery.cell.entropy_heat_fraction 
    
    return 