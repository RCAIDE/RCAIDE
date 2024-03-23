## @ingroup Library-Methods-Mission-Common-Update  
# RCAIDE/Library/Methods/Missions/Common/Update/altitude.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  Update Altitude
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Mission-Common-Update 
def altitude(segment):
    """ Updates freestream altitude from inertial position
        
        Assumptions:
        N/A
        
        Inputs:
            segment.state.conditions:
                frames.inertial.position_vector [meters]
        Outputs:
            segment.state.conditions:
                freestream.altitude             [meters]
      
        Properties Used:
        N/A
                    
    """    
    altitude = -segment.state.conditions.frames.inertial.position_vector[:,2]
    segment.state.conditions.freestream.altitude[:,0] = altitude 


def _altitude(State, Settings, System):
	'''
	Framework version of altitude.
	Wraps altitude with State, Settings, System pack/unpack.
	Please see altitude documentation for more details.
	'''

	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = altitude('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System