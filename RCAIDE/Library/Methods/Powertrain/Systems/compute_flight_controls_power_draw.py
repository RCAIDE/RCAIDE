# RCAIDE/Library/Methods/Powertrain/Systems/compute_flight_controls_power_draw.py
# 
# Created:  May 2026, M. Clarke, S. Sharma

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    
# package imports
def compute_flight_controls_power_draw(flight_controls,state,bus,conditions):
    """
    Computes the power draw of a flight controls system.
    
    Parameters
    ----------
    flight_controls : Flight_Controls
        The flight controls component with the following attributes:
            - power_draw : float
                Power consumption of the flight controls component [W]
    flight_controls_conditions : Conditions
        Object to store flight controls power conditions with the following attributes:
            - power : numpy.ndarray
                Array to store the computed power draw values [W]
    conditions : Conditions
        Object containing mission conditions (not directly used in this function)
    
    Returns
    -------
    None
        This function modifies the flight_controls_conditions.power array in-place.
    
    Notes
    -----
    This function assigns the constant power draw value from the flight controls component
    to the power array in the flight_controls_conditions object. The power draw is assumed
    to be constant throughout the mission segment.
    
    For more complex flight controls models, this function could be extended to calculate
    power draw based on operating mode, altitude, or other mission parameters.
    
    See Also
    --------
    RCAIDE.Library.Methods.Powertrain.Systems.append_flight_controls_conditions
    """
    vehicle   =  state.analyses.vehicle
    conditions = state.conditions
    
    hinge_moment       = 0    # Need Value
    angular_velocity   = 0    # Need Value
    eta_actuator       = 0.65 # Standard EHA efficiency
    eta_mech           = flight_controls.efficiency
    
    P_act =  0
    for wing in vehicle.wings:
        for control_surface in  wing.control_surfaces: 
            hinge_moment      = conditions.control_surfaces[control_surface.tag].hinge_moment
            angular_velocity  = control_surface.angular_velocity
         
            P_act            += (hinge_moment * angular_velocity) / eta_actuator 
            
    bus_conditions                        = conditions.energy.busses[bus.tag]
    flight_controls_conditions            = bus_conditions[flight_controls.tag]    
    flight_controls_conditions.power[:,0] = P_act
    bus_conditions.power_draw            += flight_controls_conditions.power*bus.power_split_ratio /bus.efficiency    
    
    return 