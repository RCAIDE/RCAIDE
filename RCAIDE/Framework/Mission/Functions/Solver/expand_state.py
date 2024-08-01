# RCAIDE/Library/Missions/Segments/expand_state.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created: Jun 2024, RCAIDE Team

# ----------------------------------------------------------------------------------------------------------------------
# Expand State
# ----------------------------------------------------------------------------------------------------------------------  
def expand_state(segment):
    
    """Makes all vectors in the state the same size.

    Assumptions:
    None

    Source:
    None

    Args:
    state.numerics.number_of_control_points  [unitless]

    Returns:
    None


    """       

    n_points = segment.state.numerics.number_of_control_points
    
    segment.state.expand_rows(n_points)
    
    return
    