## @ingroup Library-Methods-Energy-Battery 
# RCAIDE/Library/Methods/Energy/Sources/Battery/Common/pack_battery_conditions.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  pack_battery_conditions
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Energy-Battery 
def pack_battery_conditions(battery_conditions,battery): 
    """ Packs the results from the network into propulsion data structures.
    
        Assumptions:
        None
    
        Source:
        N/A
    
        Inputs: 
        battery.
               inputs.current                  [Amperes]
               current_energy                  [Joules]
               voltage_open_circuit            [Volts]
               voltage_under_load              [Volts] 
               inputs.power                    [Watts]
               maximum_energy                  [Joules]
               age                             [days]
               internal_resistance             [Ohms]
               state_of_charge                 [unitless]
               pack.temperature                [Kelvin]
               mass_properties.mass            [kilograms] 
               heat_energy_generated           [Joules]
               cell.charge_throughput          [Ampere-hours]
               cell.voltage_under_load         [Volts]  
               cell.voltage_open_circuit       [Volts]  
               cell.current                    [Amperes]
               cell.temperature                [Kelvin] 
               cell.joule_heat_fraction        [unitless]  
               cell.entropy_heat_fraction      [unitless] 
               
        Outputs:
            conditions.energy.   
               electronics_efficiency             [unitless]
               payload_efficiency                 [unitless]
               battery.pack.specfic_power         [Watt-hours/kilogram]  
                       current                    [Amperes]
                       energy                     [Joules]     
                       voltage_open_circuit       [Volts]     
                       voltage_under_load         [Volts]      
                       power_draw                 [Watts]          
                       cycle_day                  [unitless]
                       internal_resistance        [Ohms]
                       state_of_charge            [unitless]
                       pack.temperature           [Kelvin]
                       efficiency                 [unitless]
                       pack.heat_energy_generated [Joules]
                       cell.power                 [Watts]
                       cell.energy                [Joules]
                       cell.voltage_under_load    [Volts]  
                       cell.voltage_open_circuit  [Volts]  
                       cell.current               [Amperes]
                       cell.temperature           [Kelvin]
                       cell.charge_throughput     [Ampere-Hours]
                       cell.joule_heat_fraction   [unitless]  
                       cell.entropy_heat_fraction [unitless] 
    
        Properties Used:
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