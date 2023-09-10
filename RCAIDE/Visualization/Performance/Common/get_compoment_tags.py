## @ingroup Visualization-Performance-Common 
# RCAIDE/Visualization/Performance/Common/get_compoment_tags.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------    
## @ingroup Visualization-Performance-Common 
def get_propulsor_group_names(results):
    """This compile a list of propulsor groups tags within all networks on an aircraft 

    Assumptions:
    None

    Source:
    None

    Inputs 
    results data structure  [-]

    Outputs: 
    propulsor_group_names   [string[s]]

    Properties Used:
    N/A
    """
    
    pg = []
    for i in range(len(results.segments)):  
        for network in results.segments[i].analyses.energy.networks: 
            busses  = network.busses
            for bus in busses: 
                active_propulsor_groups   = bus.active_propulsor_groups     
                for j in range(len(active_propulsor_groups)):   
                    if active_propulsor_groups[j] not in pg: 
                        pg.append(active_propulsor_groups[j]) 
    return pg

def get_battery_names(results):
    """This compile a list of battery tags within all networks on an aircraft 

    Assumptions:
    None

    Source:
    None

    Inputs 
    results data structure  [-]

    Outputs: 
    battery_tags            [string[s]]

    Properties Used:
    N/A
    """
    
    bat_tags = []
    for i in range(len(results.segments)):  
        for network in results.segments[i].analyses.energy.networks: 
            busses  = network.busses
            for bus in busses: 
                for battery in bus.batteries: 
                    if battery.tag not in bat_tags: 
                        bat_tags.append(battery.tag) 
    return bat_tags