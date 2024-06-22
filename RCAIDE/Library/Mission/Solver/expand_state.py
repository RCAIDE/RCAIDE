## @ingroup Library-Missions-Segments 
# RCAIDE/Library/Missions/Segments/expand_state.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke   

# ----------------------------------------------------------------------------------------------------------------------
# Expand State
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Missions-Segments 
def expand_state(segment):
    
    """Makes all vectors in the state the same size.

    Assumptions:
    N/A

    Source:
    N/A

    Args:
    state.numerics.number_of_control_points  [Unitless]

    Returns:
    N/A


    """       

    n_points = segment.state.numerics.number_of_control_points
    
    segment.state.expand_rows(n_points)
    
    return
    