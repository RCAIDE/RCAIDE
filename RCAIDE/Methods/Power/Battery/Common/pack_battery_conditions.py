# RCAIDE/Methods/Power/Battery/Common/pack_battery_conditions.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Power-Battery 
def pack_battery_conditions(conditions,battery,avionics_payload_power): 
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
               inputs.power_in                 [Watts]
               max_energy                      [Joules]
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
                       max_aged_energy            [Joules]        
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
    battery_power_draw = battery.inputs.power_in    
       
    conditions.energy.payload_efficiency                   = (battery_power_draw+avionics_payload_power)/battery_power_draw  
    conditions.energy.battery.pack.current                 = battery.inputs.current
    conditions.energy.battery.pack.energy                  = battery.pack.current_energy
    conditions.energy.battery.pack.voltage_open_circuit    = battery.pack.voltage_open_circuit
    conditions.energy.battery.pack.voltage_under_load      = battery.pack.voltage_under_load 
    conditions.energy.battery.pack.power_draw              = battery_power_draw 
    conditions.energy.battery.pack.max_aged_energy         = battery.pack.max_energy  
    conditions.energy.battery.pack.temperature             = battery.pack.temperature  
    conditions.energy.battery.pack.heat_energy_generated   = battery.pack.heat_energy_generated
    conditions.energy.battery.pack.efficiency              = (battery_power_draw+battery.pack.resistive_losses)/battery_power_draw          
    conditions.energy.battery.pack.specfic_power           = -battery_power_draw/battery.mass_properties.mass   
    conditions.energy.battery.pack.internal_resistance     = battery.pack.internal_resistance 
    conditions.energy.battery.cell.cycle_in_day            = battery.cell.age
    conditions.energy.battery.cell.state_of_charge         = battery.cell.state_of_charge 
    conditions.energy.battery.cell.power                   = battery.inputs.power_in/n_series
    conditions.energy.battery.cell.energy                  = battery.pack.current_energy/n_total   
    conditions.energy.battery.cell.voltage_under_load      = battery.cell.voltage_under_load    
    conditions.energy.battery.cell.voltage_open_circuit    = battery.cell.voltage_open_circuit  
    conditions.energy.battery.cell.current                 = abs(battery.cell.current)        
    conditions.energy.battery.cell.temperature             = battery.cell.temperature
    conditions.energy.battery.cell.charge_throughput       = battery.cell.charge_throughput
    conditions.energy.battery.cell.joule_heat_fraction     = battery.cell.joule_heat_fraction   
    conditions.energy.battery.cell.entropy_heat_fraction   = battery.cell.entropy_heat_fraction 
    
    return 