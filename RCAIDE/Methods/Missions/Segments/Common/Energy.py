# RCAIDE/Methods/Missions/Segments/Common/Energy.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
import RCAIDE

# ----------------------------------------------------------------------------------------------------------------------
#  initialize_battery
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Methods-Missions-Segments-Common
def initialize_battery(segment):
    """ Sets the initial battery energy at the start of the mission

        Assumptions:
        N/A

        Inputs:
            segment.state.initials.conditions:
                propulsion.battery.pack.energy    [Joules]
            segment.initial_battery_state_of_charge   [Joules]

        Outputs:
            segment.state.conditions:
                propulsion.battery.pack.energy    [Joules]

        Properties Used:
        N/A

    """ 

    conditions = segment.state.conditions.energy
    
    # loop through batteries in networks
    for network in segment.analyses.energy.networks: 
        busses  = network.busses
        for bus in busses:
            for battery in bus.batteries:   
                if segment.state.initials:  
                    battery_initials                                        = segment.state.initials.conditions.energy[bus.tag][battery.tag] 
                    battery_conditions                                      = conditions[bus.tag][battery.tag]
                    initial_mission_energy                                  = battery_initials.pack.maximum_initial_energy
                    battery_capacity_fade_factor                            = battery_initials.cell.capacity_fade_factor 
                    if type(segment) ==  RCAIDE.Analyses.Mission.Segments.Ground.Battery_Recharge:            
                        battery_maximum_degraded_battery_energy             = initial_mission_energy*battery_capacity_fade_factor
                        battery_conditions.battery_discharge_flag           = False 
                    else:                  
                        battery_maximum_degraded_battery_energy             = battery_initials.pack.maximum_degraded_battery_energy  
                        battery_conditions.battery_discharge_flag           = True             
                    battery_conditions.pack.maximum_initial_energy          = initial_mission_energy
                    battery_conditions.pack.maximum_degraded_battery_energy = battery_maximum_degraded_battery_energy
                    battery_conditions.pack.energy[:,0]                     = battery_initials.pack.energy[-1,0]
                    battery_conditions.pack.temperature[:,0]                = battery_initials.pack.temperature[-1,0]
                    battery_conditions.cell.temperature[:,0]                = battery_initials.cell.temperature[-1,0]
                    battery_conditions.cell.cycle_in_day                    = battery_initials.cell.cycle_in_day      
                    battery_conditions.cell.charge_throughput[:,0]          = battery_initials.cell.charge_throughput[-1,0]
                    battery_conditions.cell.resistance_growth_factor        = battery_initials.cell.resistance_growth_factor 
                    battery_conditions.cell.capacity_fade_factor            = battery_capacity_fade_factor 

                if 'battery_cell_temperature' in segment: 
                    battery_conditions                             = conditions[battery.tag]        
                    battery_conditions.pack.temperature[:,0]       = segment.battery_cell_temperatures 
                    battery_conditions.cell.temperature[:,0]       = segment.battery_cell_temperatures 

# ----------------------------------------------------------------------
#  Update Thrust
# ----------------------------------------------------------------------

## @ingroup Methods-Missions-Segments-Common
def update_thrust(segment):
    """ Evaluates the energy network to find the thrust force and mass rate
        Inputs -
            segment.analyses.energy                     [Function]
        Outputs -
            state.conditions:
               frames.body.thrust_force_vector          [Newtons]
               weights.vehicle_mass_rate                [kg/s]
               weights.vehicle_fuel_rate                [kg/s]
               weights.vehicle_additional_fuel_rate     [kg/s]
               weights.has_additional_fuel              
        Assumptions -
    """    

    # unpack
    energy_model = segment.analyses.energy

    # evaluate
    results   = energy_model.evaluate_thrust(segment.state)

    # pack conditions
    conditions = segment.state.conditions
    conditions.frames.body.thrust_force_vector       = results.thrust_force_vector
    conditions.weights.vehicle_mass_rate             = results.vehicle_mass_rate 

    if "vehicle_additional_fuel_rate" in results: 
        conditions.weights.has_additional_fuel             = True
        conditions.weights.vehicle_fuel_rate               = results.vehicle_fuel_rate
        conditions.weights.vehicle_additional_fuel_rate    = results.vehicle_additional_fuel_rate 


def update_battery_state_of_health(segment):  
    """Updates battery age based on operating conditions, cell temperature and time of operation.
       Source: 
       Cell specific. See individual battery cell for more details

       Assumptions:
       Cell specific. See individual battery cell for more details

       Inputs: 
       segment.
           conditions                         - conditions of battery at each segment  [unitless]
           increment_battery_age_by_one_day   - flag to increment battery cycle day    [boolean]

       Outputs:
       N/A  

       Properties Used:
       N/A 
    """ 
    increment_day = segment.increment_battery_age_by_one_day

    # loop throuh networks in vehicle 
    for network in segment.analyses.energy.networks: 
        busses  = network.busses
        for bus in busses:
            for battery in bus.batteries: 
                battery_conditions  = segment.conditions.energy[bus.tag][battery.tag] 
                battery.update_battery_state_of_health(battery_conditions,increment_battery_age_by_one_day = increment_day) 