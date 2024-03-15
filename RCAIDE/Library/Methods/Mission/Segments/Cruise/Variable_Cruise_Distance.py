## @ingroup Library-Methods-Mission-Segments-Cruise
# RCAIDE/Library/Methods/Missions/Segments/Cruise/Variable_Cruise_Distance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke   

# ----------------------------------------------------------------------------------------------------------------------
# Initialize - for cruise distance
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Mission-Segments-Cruise
def initialize_cruise_distance(segment):
    """This is a method that allows your vehicle to land at prescribed landing weight

    Assumptions:
    N/A

    Source:
    N/A

    Inputs:
    segment.cruise_tag              [string]
    segment.distance                [meters]

    Outputs:
    state.unknowns.cruise_distance  [meters]

    Properties Used:
    N/A
    """         
    
    # unpack
    cruise_tag = segment.cruise_tag
    distance   = segment.segments[cruise_tag].distance
    
    # apply, make a good first guess
    segment.state.unknowns.cruise_distance = distance
    
    return

# ---------------------------------------------------------------------------------------------------------------------- 
#   Unknowns - for cruise distance
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Mission-Segments-Cruise
def unknown_cruise_distance(segment):
    """This is a method that allows your vehicle to land at prescribed landing weight

    Assumptions:
    N/A

    Source:
    N/A

    Inputs:
    segment.cruise_tag              [string]
    state.unknowns.cruise_distance  [meters]

    Outputs:
    segment.distance                [meters]

    Properties Used:
    N/A
    """      
    
    # unpack
    distance = segment.state.unknowns.cruise_distance
    cruise_tag = segment.cruise_tag
    
    # apply the unknown
    segment.segments[cruise_tag].distance = distance
    
    return


# ---------------------------------------------------------------------------------------------------------------------- 
#   Residuals - for Take Off Weight
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Mission-Segments-Cruise
def residual_landing_weight(segment):
    """This is a method that allows your vehicle to land at prescribed landing weight.
    This takes the final weight and compares it against the prescribed landing weight.

    Assumptions:
    N/A

    Source:
    N/A

    Inputs:
    segment.state.segments[-1].conditions.weights.total_mass [kilogram]
    segment.target_landing_weight                            [kilogram]

    Outputs:
    segment.state.residuals.landing_weight                   [kilogram]

    Properties Used:
    N/A
    """      
    
    # unpack
    landing_weight = segment.segments[-1].state.conditions.weights.total_mass[-1]
    target_weight  = segment.target_landing_weight
    
    # this needs to go to zero for the solver to complete
    segment.state.residuals.landing_weight = (landing_weight - target_weight)/target_weight
    
    return

# ---------------------------------------------------------------------------------------------------------------------- 
#   Residuals - for Take Off Weight
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Mission-Segments-Cruise
def residual_state_of_charge(segment):
    """This is a method that allows your vehicle to land at a prescribed state of charge.
    This takes the final weight and compares it against the prescribed state of charge.

    Assumptions:
    N/A

    Source:
    N/A

    Inputs:
    segment.state.segments[-1].conditions.energy.battery.cell.state_of_charge [None]
    segment.target_state_of_charge                                           [None]

    Outputs:
    segment.state.residuals.battery_state_of_charge                          [None]

    Properties Used:
    N/A
    """      
    
    # unpack
    end_SOC    = segment.segments[-1].state.conditions.energy.battery.cell.state_of_charge[-1]
    target_SOC = segment.target_state_of_charge
    
    # this needs to go to zero for the solver to complete
    segment.state.residuals.battery_state_of_charge = (end_SOC - target_SOC)/target_SOC
    
    return
    

    
    


def _initialize_cruise_distance(State, Settings, System):
	'''
	Framework version of initialize_cruise_distance.
	Wraps initialize_cruise_distance with State, Settings, System pack/unpack.
	Please see initialize_cruise_distance documentation for more details.
	'''

	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = initialize_cruise_distance('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System


def _unknown_cruise_distance(State, Settings, System):
	'''
	Framework version of unknown_cruise_distance.
	Wraps unknown_cruise_distance with State, Settings, System pack/unpack.
	Please see unknown_cruise_distance documentation for more details.
	'''

	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = unknown_cruise_distance('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System


def _residual_landing_weight(State, Settings, System):
	'''
	Framework version of residual_landing_weight.
	Wraps residual_landing_weight with State, Settings, System pack/unpack.
	Please see residual_landing_weight documentation for more details.
	'''

	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = residual_landing_weight('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System


def _residual_state_of_charge(State, Settings, System):
	'''
	Framework version of residual_state_of_charge.
	Wraps residual_state_of_charge with State, Settings, System pack/unpack.
	Please see residual_state_of_charge documentation for more details.
	'''

	#TODO: segment = [Replace With State, Settings, or System Attribute]

	results = residual_state_of_charge('segment',)
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System