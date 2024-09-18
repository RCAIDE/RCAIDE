## @ingroup Methods-Energy-Sources-Battery 
# RCAIDE/Methods/Energy/Sources/Battery/Common/append_battery_conditions.py
# 
# 
# Created:  Jul 2023, M. Clarke
# Modified: Sep 2024, S. Shekar

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE 
from RCAIDE.Framework.Mission.Common     import   Conditions

# ----------------------------------------------------------------------------------------------------------------------
#  METHODS
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Energy-Sources-Battery 
def append_battery_conditions(battery,segment,bus): 
    """ Packs the initial battery conditions
    
        Assumptions:
        Battery temperature is set to one degree hotter than ambient 
        temperature for robust convergence. Initial mission energy, maxed aged energy, and 
        initial segment energy are the same. Cycle day is zero unless specified, resistance_growth_factor and
        capacity_fade_factor is one unless specified in the segment
    
        Source:
        N/A
    
        Inputs:  
            atmosphere.temperature             [Kelvin]
            
            Optional:
            segment.
                 battery.cycle_in_day               [unitless]
                 battery.pack.temperature           [Kelvin]
                 battery.charge_throughput          [Ampere-Hours] 
                 battery.resistance_growth_factor   [unitless]
                 battery.capacity_fade_factor       [unitless]
                 battery.discharge                  [boolean]
                 increment_battery_age_by_one_day   [boolean]
               
        Outputs:
            segment
               battery_discharge                    [boolean]
               increment_battery_age_by_one_day     [boolean]
               segment.state.conditions.energy
               battery.battery_discharge_flag       [boolean]
               battery.pack.maximum_initial_energy  [watts]
               battery.pack.energy                  [watts] 
               battery.pack.temperature             [kelvin]
               battery.cycle_in_day                 [int]
               battery.cell.charge_throughput       [Ampere-Hours] 
               battery.resistance_growth_factor     [unitless]
               battery.capacity_fade_factor         [unitless] 
    
        Properties Used:
        None
    """
 
    ones_row                                               = segment.state.ones_row

    # compute ambient conditions
    atmosphere    = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
    alt           = -segment.conditions.frames.inertial.position_vector[:,2] 
    if segment.temperature_deviation != None:
        temp_dev = segment.temperature_deviation    
    atmo_data    = atmosphere.compute_values(altitude = alt,temperature_deviation=temp_dev)  
        
    bus_results                                            = segment.state.conditions.energy[bus.tag]        
    bus_results[battery.tag]                               = Conditions() 
    bus_results[battery.tag].pack                          = Conditions() 
    bus_results[battery.tag].cell                          = Conditions()     
    bus_results[battery.tag].pack.voltage_open_circuit     = 0 * ones_row(1)  
    bus_results[battery.tag].pack.voltage_under_load       = 0 * ones_row(1)  
    bus_results[battery.tag].pack.power                    = 0 * ones_row(1) 
    bus_results[battery.tag].pack.power_draw               = 0 * ones_row(1)    
    bus_results[battery.tag].pack.current_draw             = 0 * ones_row(1)    
    bus_results[battery.tag].pack.charging_current         = 0 * ones_row(1)    
    bus_results[battery.tag].pack.current                  = 0 * ones_row(1)    
    bus_results[battery.tag].pack.heat_energy_generated    = 0 * ones_row(1)   
    bus_results[battery.tag].pack.internal_resistance      = 0 * ones_row(1)   
    bus_results[battery.tag].cell.heat_energy_generated    = 0 * ones_row(1)    
    bus_results[battery.tag].cell.power                    = 0 * ones_row(1)         
    bus_results[battery.tag].cell.energy                   = 0 * ones_row(1)         
    bus_results[battery.tag].cell.voltage_under_load       = 0 * ones_row(1)         
    bus_results[battery.tag].cell.voltage_open_circuit     = 0 * ones_row(1)        
    bus_results[battery.tag].cell.current                  = 0 * ones_row(1)  
    bus_results[battery.tag].cell.cycle_in_day             = 0
    bus_results[battery.tag].cell.resistance_growth_factor = 1.
    bus_results[battery.tag].cell.capacity_fade_factor     = 1. 
    
    # Conditions for recharging battery 
    if type(segment) == RCAIDE.Framework.Mission.Segments.Ground.Battery_Recharge:
        segment.state.conditions.energy.recharging  = True 
        segment.state.unknowns['recharge']          =  0* ones_row(1)  
        segment.state.residuals.network['recharge'] =  0* ones_row(1) 
            
        bus_results[battery.tag].pack.charging_current = segment.current * ones_row(1)  
    elif type(segment) == RCAIDE.Framework.Mission.Segments.Ground.Battery_Discharge:
        segment.state.conditions.energy.recharging  = False 
        segment.state.unknowns['discharge']          =  0* ones_row(1)  
        segment.state.residuals.network['discharge'] =  0* ones_row(1) 
        bus_results[battery.tag].pack.charging_current = -segment.current * ones_row(1)
    else:
        segment.state.conditions.energy.recharging  = False 
        
    # first segment 
    if 'initial_battery_state_of_charge' in segment:  
        initial_battery_energy                                 = segment.initial_battery_state_of_charge*battery.pack.maximum_energy   
        bus_results[battery.tag].pack.maximum_initial_energy   = initial_battery_energy
        bus_results[battery.tag].pack.energy                   = initial_battery_energy*segment.initial_battery_state_of_charge* ones_row(1) 
        bus_results[battery.tag].cell.state_of_charge          = segment.initial_battery_state_of_charge* ones_row(1) 
        bus_results[battery.tag].cell.depth_of_discharge       = 1 - segment.initial_battery_state_of_charge* ones_row(1)
    else:  
        bus_results[battery.tag].pack.energy                   = 0 * ones_row(1) 
        bus_results[battery.tag].cell.state_of_charge          = 0 * ones_row(1)       
        bus_results[battery.tag].cell.depth_of_discharge       = 0 * ones_row(1)   
        
    # temperature 
    if 'battery_cell_temperature' in segment:
        cell_temperature  = segment.battery_cell_temperature  
    else:
        cell_temperature  = atmo_data.temperature[0,0] 
    bus_results[battery.tag].pack.temperature              = cell_temperature * ones_row(1)         
    bus_results[battery.tag].cell.temperature              = cell_temperature * ones_row(1) 

    # charge thoughput 
    if 'charge_throughput' in segment: 
        bus_results[battery.tag].cell.charge_throughput  = segment.charge_throughput * ones_row(1)  
    else:
        bus_results[battery.tag].cell.charge_throughput  = 0 * ones_row(1)  
        
    # This is the only one besides energy and discharge flag that should be packed into the segment top level
    if 'increment_battery_age_by_one_day' not in segment:
        segment.increment_battery_age_by_one_day   = False    
     
    return 
    
def append_battery_segment_conditions(battery, bus, conditions, segment): 
    """Sets the initial battery energy at the start of each segment as the last point from the previous segment 
    
        Assumptions:
        None
    
        Source:
        N/A
    
        Inputs:  
         battery          (data structure)              [None]
               
        Outputs:
        None
    
        Properties Used:
        None
    """

    battery_conditions = conditions[bus.tag][battery.tag]
    if segment.state.initials:  
        battery_initials                                        = segment.state.initials.conditions.energy[bus.tag][battery.tag]  
        if type(segment) ==  RCAIDE.Framework.Mission.Segments.Ground.Battery_Recharge:             
            battery_conditions.battery_discharge_flag           = False 
        else:                   
            battery_conditions.battery_discharge_flag           = True             
        battery_conditions.pack.maximum_initial_energy          = battery_initials.pack.maximum_initial_energy 
        battery_conditions.pack.energy[:,0]                     = battery_initials.pack.energy[-1,0]
        battery_conditions.pack.temperature[:,0]                = battery_initials.pack.temperature[-1,0]
        battery_conditions.cell.temperature[:,0]                = battery_initials.cell.temperature[-1,0]
        battery_conditions.cell.cycle_in_day                    = battery_initials.cell.cycle_in_day      
        battery_conditions.cell.charge_throughput[:,0]          = battery_initials.cell.charge_throughput[-1,0]
        battery_conditions.cell.resistance_growth_factor        = battery_initials.cell.resistance_growth_factor 
        battery_conditions.cell.capacity_fade_factor            = battery_initials.cell.capacity_fade_factor 
        battery_conditions.cell.state_of_charge[:,0]            = battery_initials.cell.state_of_charge[-1,0]

    if 'battery_cell_temperature' in segment:       
        battery_conditions.pack.temperature[:,0]       = segment.battery_cell_temperature 
        battery_conditions.cell.temperature[:,0]       = segment.battery_cell_temperature     

    return    