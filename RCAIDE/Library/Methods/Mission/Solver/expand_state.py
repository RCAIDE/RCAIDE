## @ingroup Library-Methods-Mission-Segments 
# RCAIDE/Library/Methods/Missions/Segments/expand_state.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke   

# ----------------------------------------------------------------------------------------------------------------------
# Expand State
# ---------------------------------------------------------------------------------------------------------------------- 
## @ingroup Library-Methods-Mission-Segments 
def expand_state(segment):
    
    """Makes all vectors in the state the same size.

    Assumptions:
    N/A

    Source:
    N/A

    Inputs:
    state.numerics.number_of_control_points  [Unitless]

    Outputs:
    N/A

    Properties Used:
    N/A
    """       

    n_points = segment.state.numerics.number_of_control_points
    
    segment.state.expand_rows(n_points)
    
    return
    