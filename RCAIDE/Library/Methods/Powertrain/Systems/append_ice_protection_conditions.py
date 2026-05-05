# RCAIDE/Library/Methods/Powertrain/Systems/append_ice_protection_conditions.py
# 
# Created:  May 2026, M. Clarke, S. Sharma 

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_ice_protection_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_ice_protection_conditions(ice_protection, segment, bus):  
    """Initializes and appends empty ice protection conditions data structures to the segment state conditions.

    Parameters
    ----------
    ice_protection : Ice_Protection
        The ice protection component for which conditions are being initialized.
    segment : Segment
        The mission segment in which the ice protection systems are operating.
    bus : ElectricalBus
        The electrical bus that powers the ice protection system.

    Returns
    -------
    None
    
    Notes
    -----
    This function creates an empty Conditions object for the ice protection system within
    the segment's energy conditions dictionary, indexed by the bus tag and ice protection tag.

    The ice protection power consumption is initialized as a zero array with the same
    length as the segment's state vector. This will be updated during mission analysis
    based on the ice protection power requirements.
    
    See Also
    -------- 
    """
    ones_row    = segment.state.ones_row
    segment.state.conditions.energy.busses[bus.tag][ice_protection.tag]            = Conditions()
    segment.state.conditions.energy.busses[bus.tag][ice_protection.tag].power      = 0 * ones_row(1)
    
    return
