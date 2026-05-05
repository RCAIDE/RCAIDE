# RCAIDE/Library/Methods/Powertrain/Systems/compute_ice_protection_power_draw.py
# 
# Created:  May 2026, M. Clarke, S. Sharma

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    
# package imports
def compute_ice_protection_power_draw(ice_protection,state,bus,conditions):
    """
    Computes the power draw of an ice protection system.
    
    Parameters
    ----------
    ice_protection : Ice_Protection
        The ice protection component with the following attributes:
            - power_draw : float
                Power consumption of the ice protection component [W]
    bus : ElectricalBus
        The electrical bus that powers the ice protection system.
    conditions : Conditions
        Object containing mission conditions (not directly used in this function)

    Returns
    -------
    None
        This function modifies the ice_protection_conditions.power array in-place.

                Array to store the computed power draw values [W]
    conditions : Conditions
        Object containing mission conditions (not directly used in this function)
    
    Returns
    -------
    None
        This function modifies the ice_protection_conditions.power array in-place.
    
    Notes
    -----
    This function assigns the constant power draw value from the ice protection component
    to the power array in the ice_protection_conditions object. The power draw is assumed
    to be constant throughout the mission segment.
    
    For more complex ice protection models, this function could be extended to calculate
    power draw based on operating mode, altitude, or other mission parameters.
    
    See Also
    --------
    RCAIDE.Library.Methods.Powertrain.Systems.append_ice_protection_conditions
    """
    Area           = 0
    percentage_ice = 0.05 # 5% of the wing is leading edge
    
    # EMEDI Constants (Example values)
    E_pulse      = 500    # Joules per pulse
    f_pulse      = 0.2    # Pulses per second (12 per minute)
    eta_sys      = 0.8    # 80% efficiency
    q_total_flux = 15000  # W/m², Total heat flux required to prevent ice accretion (convective + evaporative + sensible) (approx 15 kW/m^2)
    
    q_convective = 0
    q_evaporative = 0
    q_sensible  = 0
    
    vehicle   = state.analyses.vehicle    
    for wing in vehicle.wings:
        Area += wing.reference_area * percentage_ice 
 
    # P_anti_ice = Area * (q_convective + q_evaporative + q_sensible)
    P_anti_ice = Area * q_total_flux
    P_de_ice   = (E_pulse * f_pulse) / eta_sys     
    
    P_ice      =  P_anti_ice + P_de_ice
    
    bus_conditions                       = conditions.energy.busses[bus.tag]
    ice_protection_conditions            = bus_conditions[ice_protection.tag]    
    ice_protection_conditions.power[:,0] = P_ice
    bus_conditions.power_draw           += ice_protection_conditions.power*bus.power_split_ratio /bus.efficiency    
    
    return 