# RCAIDE/Library/Methods/Powertrain/Systems/append_flight_controls_conditions.py
# 
# Created:  Jun 2024, M. Clarke  

from RCAIDE.Framework.Mission.Common     import   Conditions

# ---------------------------------------------------------------------------------------------------------------------- 
#  append_flight_controls_conditions
# ----------------------------------------------------------------------------------------------------------------------    
def append_flight_controls_conditions(flight_controls, segment, bus):  
    """
    Initializes and appends empty flight_controls conditions data structures to the segment state conditions.
    
    Parameters
    ----------
    flight_controls : flight_controls
        The flight_controls component for which conditions are being initialized.
    segment : Segment
        The mission segment in which the flight_controls is operating.
    bus : ElectricalBus
        The electrical bus that powers the flight_controls system.
    
    Returns
    -------
    None
    
    Notes
    -----
    This function creates an empty Conditions object for the flight_controls system within
    the segment's energy conditions dictionary, indexed by the bus tag and flight_controls tag.
    
    The flight_controls power consumption is initialized as a zero array with the same
    length as the segment's state vector. This will be updated during mission analysis
    based on the flight_controls power requirements.
    
    See Also
    -------- 
    """
    ones_row    = segment.state.ones_row
    segment.state.conditions.energy.busses[bus.tag][flight_controls.tag]            = Conditions()
    segment.state.conditions.energy.busses[bus.tag][flight_controls.tag].power      = 0 * ones_row(1)
    
    return 
