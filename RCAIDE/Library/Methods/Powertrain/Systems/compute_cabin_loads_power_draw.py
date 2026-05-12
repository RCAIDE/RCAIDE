# RCAIDE/Library/Methods/Powertrain/Systems/compute_cabin_loads_power_draw.py
# 
# Created:  May 2026, M. Clarke, S. Sharma 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    
# package imports
def compute_cabin_loads_power_draw(cabin_loads,vehicle,bus,state):
    """
    Computes the power draw of a cabin loads system.
    
    Parameters
    ----------
    cabin_loads : Cabin_Loads
        The cabin loads component with the following attributes:
            - power_draw : float
                Power consumption of the cabin loads component [W]
    cabin_loads_conditions : Conditions
        Object to store cabin loads power conditions with the following attributes:
            - power : numpy.ndarray
                Array to store the computed power draw values [W]
    conditions : Conditions
        Object containing mission conditions (not directly used in this function)
    
    Returns
    -------
    None
        This function modifies the cabin_loads_conditions.power array in-place.
    
    Notes
    -----
    This function assigns the constant power draw value from the cabin loads component
    to the power array in the cabin_loads_conditions object. The power draw is assumed
    to be constant throughout the mission segment.
    
    For more complex cabin loads models, this function could be extended to calculate
    power draw based on operating mode, altitude, or other mission parameters.
    
    See Also
    --------
    RCAIDE.Library.Methods.Powertrain.Systems.append_cabin_loads_conditions
    """
    N_pax              = vehicle.number_of_passengers
    
    P_ife_per_pax      = 41                             # Watts
    P_galley_per_pax   = 320 * 0.5                      # Watts (For cruise segment, we can assume 50% usage factor for galley power)
    P_lighting_per_pax = 3.2 + 1.4 + 10                 # Watts (Reading Lights + Ambient Lighting + General Cabin Lighting, scales with pax)
    
    P_cabin            = (N_pax * (P_ife_per_pax + P_galley_per_pax + P_lighting_per_pax))
            
    bus_conditions                    = state.conditions.energy.busses[bus.tag]
    cabin_loads_conditions            = bus_conditions[cabin_loads.tag]    
    cabin_loads_conditions.power[:,0] = P_cabin
    bus_conditions.power_draw        += cabin_loads_conditions.power*bus.power_split_ratio /bus.efficiency    
    
    return 