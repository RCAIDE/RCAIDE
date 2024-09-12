## @ingroup Library-Missions-Segments-Common-Initialize
# RCAIDE/Library/Missions/Common/Initialize/energy.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE im
# ----------------------------------------------------------------------------------------------------------------------
#  energy
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Missions-Segments-Common-Initialize
def energy(segment):
    """ Sets the initial battery energy at the start of the mission

        Assumptions:
        N/A

        Inputs:
            segment.state.initials.conditions:
                propulsion.battery.pack.energy               [Joules]
            segment.initial_battery_state_of_charge          [Joules]
 
        Outputs: 
            segment.state.conditions: 
                energy.battery.pack.energy                   [Joules]
                energy.battery.pack.maximum_initial_energy   [Joules]     
                energy.battery.pack.energy                   [Joules]
                energy.battery.pack.temperature              [Kelvin]
                energy.battery.cell.temperature              [Kelvin]            
                energy.battery.cell.cycle_in_day             [N.A]              
                energy.battery.cell.charge_throughput        [Amp-Hrs]  
                energy.battery.cell.resistance_growth_factor [N.A]      
                energy.battery.cell.capacity_fade_factor     [N.A]      
                energy.battery.cell.state_of_charge          [N.A] 

        Properties Used:
        N/A

    """ 

    conditions = segment.state.conditions.energy
    
    # loop through batteries in networks
    for network in segment.analyses.energy.vehicle.networks:  
        # if network has busses 
        if 'busses' in network: 
            for bus in network.busses:
                for battery in bus.batteries:
                    battery.append_battery_segment_conditions(bus, conditions, segment)
            for coolant_line in  network.coolant_lines:
                for tag, item in  coolant_line.items(): 
                    if tag == 'batteries':
                        for battery in item:
                            for btms in  battery:
                                btms.append_segment_conditions(segment,coolant_line, conditions)
                    if tag == 'heat_exchangers':
                        for heat_exchanger in  item:
                            heat_exchanger.append_segment_conditions(segment, coolant_line, conditions)
                    if tag == 'reservoirs':
                        for reservoir in  item:
                            reservoir.append_segment_conditions(segment, coolant_line, conditions) 
                    
         # if network has fuel lines                        
        elif 'fuel_lines' in network: 
            for fuel_line in  network.fuel_lines:
                for fuel_tank in fuel_line.fuel_tanks: 
                    fuel_tank_conditions   = conditions[fuel_line.tag][fuel_tank.tag] 
                    if segment.state.initials:  
                        fuel_tank_initials = segment.state.initials.conditions.energy[fuel_line.tag][fuel_tank.tag] 
                        fuel_tank_conditions.mass[:,0]   = fuel_tank_initials.mass[-1,0]
                    else: 
                        fuel_tank_conditions.mass[:,0]   = segment.analyses.energy.vehicle.networks[network.tag].fuel_lines[fuel_line.tag].fuel_tanks[fuel_tank.tag].fuel.mass_properties.mass
            
                    
