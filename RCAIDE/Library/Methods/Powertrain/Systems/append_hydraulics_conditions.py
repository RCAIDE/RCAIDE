# RCAIDE/Library/Methods/Powertrain/Systems/append_hydraulics_conditions.py
# 
# Created:  May 2026, M. Clarke, S. Sharma 

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_hydraulics_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_hydraulics_conditions(hydraulics, segment, bus):  
    """
    Initializes and appends empty hydraulic systems conditions data structures to the segment state conditions.

    Parameters
    ----------
    hydraulics : Hydraulics
        The hydraulic systems component for which conditions are being initialized.
    segment : Segment
        The mission segment in which the hydraulic systems are operating.
    bus : ElectricalBus
        The electrical bus that powers the hydraulic systems system.

    Returns
    -------
    None
    
    Notes
    -----
    This function creates an empty Conditions object for the hydraulic systems system within
    the segment's energy conditions dictionary, indexed by the bus tag and hydraulic systems tag.

    The hydraulic systems power consumption is initialized as a zero array with the same
    length as the segment's state vector. This will be updated during mission analysis
    based on the hydraulic systems power requirements.
    
    See Also
    -------- 
    """
    ones_row    = segment.state.ones_row
    segment.state.conditions.energy.busses[bus.tag][hydraulics.tag]            = Conditions()
    segment.state.conditions.energy.busses[bus.tag][hydraulics.tag].power      = 0 * ones_row(1)
    
    return 
