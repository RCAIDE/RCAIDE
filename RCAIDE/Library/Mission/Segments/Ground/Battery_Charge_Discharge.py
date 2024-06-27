## @ingroup Library-Missions-Segments-Ground
# RCAIDE/Library/Missions/Segments/Ground/Battery_Charge_Discharge.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 
 
# ----------------------------------------------------------------------------------------------------------------------  
#  Initialize Conditions
# ----------------------------------------------------------------------------------------------------------------------  
## @ingroup Library-Missions-Segments-Ground 
def initialize_conditions(segment):  
    """Sets the specified conditions which are given for the segment type.

    Assumptions: 
    During recharging, the charge time associated with the largest capacity battery pack is used 
    
    Source:
    None

    Args:
    segment.overcharge_contingency              [-]
    battery.                                    [-]

    Returns: 
    conditions.frames.inertial.time             [seconds]


    """    
    t_nondim   = segment.state.numerics.dimensionless.control_points
    conditions = segment.state.conditions   
    
    # dimensionalize time
    t_initial = conditions.frames.inertial.time[0,0]
    t_nondim  = segment.state.numerics.dimensionless.control_points
    time      = t_nondim * ( segment.time ) + t_initial
    
    segment.state.conditions.frames.inertial.time[:,0] = time[:,0] 

