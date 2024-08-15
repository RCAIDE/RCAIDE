## @ingroup Library-Missions-Segments-Common-Pre_Process
# RCAIDE/Library/Missions/Common/Pre_Process/energy.py
# 
# 
# Created:  Jul 2023, M. Clarke
 
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
        for network in segment.analyses.energy.vehicle.networks:
            network.add_unknowns_and_residuals_to_segment(segment) 
    return 