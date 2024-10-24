# RCAIDE/Library/Missions/Common/Pre_Process/energy.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team
 
# ----------------------------------------------------------------------------------------------------------------------
#  energy
# ----------------------------------------------------------------------------------------------------------------------   
def energy(mission):
    """ Appends all unknows and residuals to the network 
    
        Assumptions:
            None
        
        Args:
            mission : data structure containing all flight segments [-]
            
        Returns:
            None  
    """       
    for segment in mission.segments:
        for network in segment.analyses.energy.vehicle.networks:
            network.add_unknowns_and_residuals_to_segment(segment) 
    return 