# RCAIDE/Library/Missions/Common/Initialize/energy.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------

# RCAIDE imports 
import RCAIDE

# ----------------------------------------------------------------------------------------------------------------------
#  energy
# ----------------------------------------------------------------------------------------------------------------------   
def energy(segment):
    """ Sets the initial energy state of the aircraft at the start of the mission

        Assumptions:
            None
        
        Args: 
            segment  : flight segment        [-] 
            
        Returns:
            None 
        """

    conditions = segment.state.conditions.energy
    
    # loop through batteries in networks
    for network in segment.analyses.energy.vehicle.networks:  
        # if network has busses 
        if 'busses' in network: 
            for bus in network.busses:
                for battery in bus.batteries:   
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
                        
        elif 'fuel_lines' in network: 
            for fuel_line in  network.fuel_lines:
                for fuel_tank in fuel_line.fuel_tanks: 
                    fuel_tank_conditions   = conditions[fuel_line.tag][fuel_tank.tag] 
                    if segment.state.initials:  
                        fuel_tank_initials = segment.state.initials.conditions.energy[fuel_line.tag][fuel_tank.tag] 
                        fuel_tank_conditions.mass[:,0]   = fuel_tank_initials.mass[-1,0]
                    else: 
                        fuel_tank_conditions.mass[:,0]   = segment.analyses.energy.vehicle.networks[network.tag].fuel_lines[fuel_line.tag].fuel_tanks[fuel_tank.tag].fuel.mass_properties.mass    
                    
