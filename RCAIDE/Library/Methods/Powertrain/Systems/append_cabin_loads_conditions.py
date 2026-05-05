# RCAIDE/Library/Methods/Powertrain/Systems/append_cabin_loads_conditions.py
# 
# Created:  May 2026, M. Clarke, S. Sharma  

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_cabin_loads_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_cabin_loads_conditions(cabin_loads, segment, bus):  
    """
    Initializes and appends empty cabin loads conditions data structures to the segment state conditions.

    Parameters
    ----------
    cabin_loads : Cabin_Loads
        The cabin loads component for which conditions are being initialized.
    segment : Segment
        The mission segment in which the cabin loads are operating.
    bus : ElectricalBus
        The electrical bus that powers the cabin loads system.

    Returns
    -------
    None
    
    Notes
    -----
    This function creates an empty Conditions object for the cabin loads system within
    the segment's energy conditions dictionary, indexed by the bus tag and cabin loads tag.

    The cabin loads power consumption is initialized as a zero array with the same
    length as the segment's state vector. This will be updated during mission analysis
    based on the cabin loads power requirements.
    
    See Also
    -------- 
    """
    ones_row    = segment.state.ones_row
    segment.state.conditions.energy.busses[bus.tag][cabin_loads.tag]            = Conditions()
    segment.state.conditions.energy.busses[bus.tag][cabin_loads.tag].power      = 0 * ones_row(1)
    
    return 
