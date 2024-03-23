## @ingroup Library-Methods-Mission-Common-Initialize
# RCAIDE/Library/Methods/Missions/Common/Initialize/weights.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke
 

# ----------------------------------------------------------------------------------------------------------------------
#  Initialize Weights
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Mission-Common-Initialize
def weights(segment):
    """ Initializes weight of vehicle
    
        Assumptions:   
            Uses max takeoff weight if no weight analysis is performed 
            
        Inputs: 
            state.
                initials.conditions.weights.total_mass  [kg]
            state.conditions:           
                conditions.weights.total_mass           [kg]
            
        Outputs: 
            state.conditions.weights.total_mass         [kg] 
           
        Properties Used:
        N/A 
    """      
 
    if segment.state.initials:
        m_initial = segment.state.initials.conditions.weights.total_mass[-1,0] 
    else: 
        if segment.analyses.weights != None: 
            m_initial = segment.analyses.weights.vehicle.mass_properties.takeoff
        else: 
            m_initial = segment.analyses.energy.networks[list(segment.analyses.energy.networks.keys())[0]].mass_properties.mass

    m_current = segment.state.conditions.weights.total_mass
    
    segment.state.conditions.weights.total_mass[:,:] = m_current + (m_initial - m_current[0,0])
        
    return 


def _weights(State, Settings, System):
	'''
	Framework version of weights.
	Wraps weights with State, Settings, System pack/unpack.
	Please see weights documentation for more details.
	'''

	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = weights('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System