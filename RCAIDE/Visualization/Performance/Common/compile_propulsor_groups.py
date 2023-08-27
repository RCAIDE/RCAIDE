
# RCAIDE/Visualization/Performance/Common/compile_propulsor_groups.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  PLOTS
# ----------------------------------------------------------------------------------------------------------------------    
## @ingroup Visualization-Performance-Common 
def compile_propulsor_groups(results):
    """This compile a list of propulsor groups within all networks on an aircraft 

    Assumptions:
    None

    Source:
    None

    Inputs
    axes

    Outputs:
    axes

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
                    if active_propulsor_groups in pg:
                        pass
                    else:
                        pg.append(active_propulsor_groups[j]) 
    return 