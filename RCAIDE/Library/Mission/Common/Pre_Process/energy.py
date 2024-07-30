## @ingroup Library-Missions-Segments-Common-Pre_Process
# RCAIDE/Library/Missions/Common/Pre_Process/energy.py
# 
# 
# Created:  Jul 2023, M. Clarke

import  RCAIDE
 
# ----------------------------------------------------------------------------------------------------------------------
#  energy
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Missions-Segments-Common-Pre_Process

def energy(mission):
    """ Appends all unknows and residuals to the network 
    
        Assumptions:
            N/A
        
        Inputs:
            None
            
        Outputs:
            None 

        Properties Used:
        N/A                
    """
    
    

    for segment in mission.segments:
        for network in segment.analyses.energy.networks:
            for distribution_line in network.distribution_lines:
                first_propulsor = True
                for propulsor in distribution_line.propulsors:
                    if first_propulsor:
                        propulsor.add_unknowns_and_residuals_to_segment(segment, distribution_line, propulsor, True)
                        first_propulsor = False
                    else:
                        propulsor.add_unknowns_and_residuals_to_segment(segment, distribution_line, propulsor, False)
                for fuel_tank in distribution_line.fuel_tanks:
                    fuel_tank.add_unknowns_and_residuals_to_segment(segment, distribution_line, fuel_tank)


    return 