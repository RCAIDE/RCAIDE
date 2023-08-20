# RCAIDE/Methods/Power/Battery/Common/append_initial_battery_conditions.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------
# RCAIDE imports 
import RCAIDE 

# ----------------------------------------------------------------------------------------------------------------------
#  METHOD
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Methods-Power-Battery 
def append_initial_battery_conditions(segment,bus,battery): 
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
                 battery_i.cycle_in_day               [unitless]
                 battery_i.pack.temperature           [Kelvin]
                 battery_i.charge_throughput          [Ampere-Hours] 
                 battery_i.resistance_growth_factor   [unitless]
                 battery_i.capacity_fade_factor       [unitless]
                 battery_i.discharge                  [boolean]
                 increment_battery_age_by_one_day     [boolean]
               
        Outputs:
            segment
               battery_discharge                      [boolean]
               increment_battery_age_by_one_day       [boolean]
            segment.state.conditions.energy
               battery_i.battery_discharge_flag               [boolean]
               battery_i.pack.maximum_initial_energy  [watts]
               battery_i.pack.energy                  [watts]
               battery_i.pack.maximum_degraded_battery_energy [watts]    
               battery_i.pack.temperature             [kelvin]
               battery_i.cycle_in_day                 [int]
               battery_i.cell.charge_throughput       [Ampere-Hours] 
               battery_i.resistance_growth_factor     [unitless]
               battery_i.capacity_fade_factor         [unitless]
               
               where i = number of batteries  

    
        Properties Used:
        None
    """       
    # compute ambient conditions
    atmosphere    = RCAIDE.Analyses.Atmospheric.US_Standard_1976()
    alt           = -segment.conditions.frames.inertial.position_vector[:,2] 
    if segment.temperature_deviation != None:
        temp_dev = segment.temperature_deviation    
    atmo_data    = atmosphere.compute_values(altitude = alt,temperature_deviation=temp_dev) 
      
    battery_conditions = segment.state.conditions.energy[bus.tag][battery.tag]
    
    # Set if it is a discharge segment
    if type(segment) ==  RCAIDE.Analyses.Mission.Segments.Ground.Battery_Recharge:  
        battery_conditions.battery_discharge_flag  = False
    else:
        battery_conditions.battery_discharge_flag  = True
        
    # This is the only one besides energy and discharge flag that should be packed into the segment top level
    if 'increment_battery_age_by_one_day' not in segment:
        segment.increment_battery_age_by_one_day   = False    
        
    # If an initial segment with battery energy set 
    if 'battery_cell_temperature' not in segment:     
        cell_temperature              = atmo_data.temperature[0,0]
    else:
        cell_temperature              = segment.battery_pack_temperature 
    battery_conditions.pack.temperature[:,0] = cell_temperature
    battery_conditions.cell.temperature[:,0] = cell_temperature 
    
    if 'maximum_degraded_battery_energy' in segment:
        maximum_degraded_battery_energy = segment.maximum_degraded_battery_energy
    else:
        maximum_degraded_battery_energy = battery.pack.maximum_energy  
    battery_conditions.pack.maximum_degraded_battery_energy = maximum_degraded_battery_energy    
        
    if 'initial_battery_state_of_charge' in segment:  
        initial_battery_energy            = segment.initial_battery_state_of_charge*battery.pack.maximum_energy 
        
        if 'battery_cycle_in_day' not in segment: 
            cycle_in_day                  = 0
        else:
            cycle_in_day                  = segment.battery_cycle_in_day

        if 'battery_cell_charge_throughput' not in segment:
            cell_charge_throughput        = 0.
        else:
            cell_charge_throughput        = segment.battery_cell_charge_throughput
            
        if 'battery_resistance_growth_factor' not in segment:
            resistance_growth_factor      = 1 
        else:
            resistance_growth_factor      = segment.battery_resistance_growth_factor
            
        if 'battery_capacity_fade_factor' not in segment: 
            capacity_fade_factor          = 1   
        else:
            capacity_fade_factor          = segment.battery_capacity_fade_factor
        
        # Pack into conditions
        battery_conditions.pack.maximum_initial_energy       = initial_battery_energy
        battery_conditions.pack.energy[:,0]                  = initial_battery_energy
        battery_conditions.cell.cycle_in_day                 = cycle_in_day        
        battery_conditions.cell.charge_throughput[:,0]       = cell_charge_throughput 
        battery_conditions.cell.resistance_growth_factor     = resistance_growth_factor 
        battery_conditions.cell.capacity_fade_factor         = capacity_fade_factor
        battery_conditions.cell.state_of_charge[:,0]         = initial_battery_energy/maximum_degraded_battery_energy
            
    return 
    
 