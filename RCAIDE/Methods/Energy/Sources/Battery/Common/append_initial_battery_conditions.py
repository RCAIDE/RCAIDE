## @ingroup Methods-Energy-Sources-Battery 
# RCAIDE/Methods/Energy/Sources/Battery/Common/append_initial_battery_conditions.py
# (c) Copyright 2023 Aerospace Research Community LLC
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
## @ingroup Methods-Energy-Sources-Battery 
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
                 battery.cycle_in_day               [unitless]
                 battery.pack.temperature           [Kelvin]
                 battery.charge_throughput          [Ampere-Hours] 
                 battery.resistance_growth_factor   [unitless]
                 battery.capacity_fade_factor       [unitless]
                 battery.discharge                  [boolean]
                 increment_battery_age_by_one_day     [boolean]
               
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
    # compute ambient conditions
    atmosphere    = RCAIDE.Analyses.Atmospheric.US_Standard_1976()
    alt           = -segment.conditions.frames.inertial.position_vector[:,2] 
    if segment.temperature_deviation != None:
        temp_dev = segment.temperature_deviation    
    atmo_data    = atmosphere.compute_values(altitude = alt,temperature_deviation=temp_dev) 
      
    battery_conditions = segment.state.conditions.energy[bus.tag][battery.tag] 
    
    # Set if it is a discharge segment
    if type(segment) ==  RCAIDE.Analyses.Mission.Segments.Ground.Battery_Recharge:  
        segment.state.conditions.energy.recharging  = True 
    else:
        segment.state.conditions.energy.recharging  = False 
        
    # This is the only one besides energy and discharge flag that should be packed into the segment top level
    if 'increment_battery_age_by_one_day' not in segment:
        segment.increment_battery_age_by_one_day   = False    
        
    # If an initial segment with battery energy set 
    if 'battery_cell_temperature' in segment:
        cell_temperature  = segment.battery_cell_temperature  
    else:
        cell_temperature  = atmo_data.temperature[0,0]
    battery_conditions.pack.temperature[:,0] = cell_temperature
    battery_conditions.cell.temperature[:,0] = cell_temperature 
    
    # charge thoughput 
    if 'charge_throughput' in segment: 
        battery_conditions.cell.charge_throughput[:,0] = segment.charge_throughput 
    else:
        battery_conditions.cell.charge_throughput[:,0] = 0
        
    if 'initial_battery_state_of_charge' in segment:  
        initial_battery_energy                               = segment.initial_battery_state_of_charge*battery.pack.maximum_energy   
        battery_conditions.pack.maximum_initial_energy       = initial_battery_energy
        battery_conditions.pack.energy[:,0]                  = initial_battery_energy*segment.initial_battery_state_of_charge
        battery_conditions.cell.state_of_charge[:,0]         = segment.initial_battery_state_of_charge
        battery_conditions.cell.depth_of_discharge[:,0]      = 1 - segment.initial_battery_state_of_charge
            
    return 
    
 