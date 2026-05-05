# RCAIDE/Library/Methods/Powertrain/Systems/append_environmental_control_conditions.py
# 
# Created:  May 2026, M. Clarke, S. Sharma  

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_environmental_control_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_environmental_control_conditions(environmental_controls, segment, bus):  
    """
    Initializes and appends empty environmental control conditions data structures to the segment state conditions.

    Parameters
    ----------
    environmental_controls : Environmental_Controls
        The environmental control component for which conditions are being initialized.
    segment : Segment
        The mission segment in which the environmental controls are operating.
    bus : ElectricalBus
        The electrical bus that powers the environmental control system.

    Returns
    -------
    None
    
    Notes
    -----
    This function creates an empty Conditions object for the environmental control system within
    the segment's energy conditions dictionary, indexed by the bus tag and environmental controls tag.

    The environmental control power consumption is initialized as a zero array with the same
    length as the segment's state vector. This will be updated during mission analysis
    based on the environmental control power requirements.
    
    See Also
    -------- 
    """
    ones_row    = segment.state.ones_row
    segment.state.conditions.energy.busses[bus.tag][environmental_controls.tag]            = Conditions()
    segment.state.conditions.energy.busses[bus.tag][environmental_controls.tag].power      = 0 * ones_row(1)
    
    return 
