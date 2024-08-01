# RCAIDE/Library/Missions/Segments/Cruise/Variable_Cruise_Distance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# Initialize - for cruise distance
# ---------------------------------------------------------------------------------------------------------------------- 

def initialize_cruise_distance(segment):
    """This is a method that allows your vehicle to land at prescribed landing weight

    Assumptions:
    None

    Source:
    None

    Args:
    segment.cruise_tag              [string]
    segment.distance                [meters]

    Returns:
    state.unknowns.cruise_distance  [meters] 
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

def unknown_cruise_distance(segment):
    """This is a method that allows your vehicle to land at prescribed landing weight

    Assumptions:
    None

    Source:
    None

    Args:
    segment.cruise_tag              [string]
    state.unknowns.cruise_distance  [meters]

    Returns:
    segment.distance                [meters] 
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

def residual_landing_weight(segment):
    """This is a method that allows your vehicle to land at prescribed landing weight.
    This takes the final weight and compares it against the prescribed landing weight.

    Assumptions:
    None

    Source:
    None

    Args:
    segment.state.segments[-1].conditions.weights.total_mass [kilogram]
    segment.target_landing_weight                            [kilogram]

    Returns:
    segment.state.residuals.landing_weight                   [kilogram] 
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

def residual_state_of_charge(segment):
    """This is a method that allows your vehicle to land at a prescribed state of charge.
    This takes the final weight and compares it against the prescribed state of charge.

    Assumptions:
    None

    Source:
    None

    Args:
    segment.state.segments[-1].conditions.energy.battery.cell.state_of_charge [None]
    segment.target_state_of_charge                                           [None]

    Returns:
    segment.state.residuals.battery_state_of_charge                          [None] 
    """      
    
    # unpack
    end_SOC    = segment.segments[-1].state.conditions.energy.battery.cell.state_of_charge[-1]
    target_SOC = segment.target_state_of_charge
    
    # this needs to go to zero for the solver to complete
    segment.state.residuals.battery_state_of_charge = (end_SOC - target_SOC)/target_SOC
    
    return
    

    
    