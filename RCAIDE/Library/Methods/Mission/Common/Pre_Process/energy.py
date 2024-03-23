## @ingroup Library-Methods-Mission-Segments-Common-Pre_Process
# RCAIDE/Library/Methods/Missions/Common/Pre_Process/energy.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 
# ----------------------------------------------------------------------------------------------------------------------
#  energy
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Methods-Mission-Segments-Common-Pre_Process
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
            network.add_unknowns_and_residuals_to_segment(segment) 
    return 


def _energy(State, Settings, System):
	'''
	Framework version of energy.
	Wraps energy with State, Settings, System pack/unpack.
	Please see energy documentation for more details.
	'''

	#TODO: mission = [Replace With State, Settings, or System Attribute]

	results = energy('mission',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System