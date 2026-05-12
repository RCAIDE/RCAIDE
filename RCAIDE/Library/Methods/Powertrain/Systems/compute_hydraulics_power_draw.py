# RCAIDE/Library/Methods/Powertrain/Systems/compute_hydraulics_power_draw.py
# 
# Created:  May 2026, M. Clarke, S. Sharma

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    
# package imports
import numpy as np

def compute_hydraulics_power_draw(hydraulics,vehicle,bus,state):
    """
    Computes the power draw of a hydraulic systems system.
    
    Parameters
    ----------
    hydraulics : Hydraulics
        The hydraulic systems component with the following attributes:
            - power_draw : float
                Power consumption of the hydraulic systems component [W]
    hydraulics_conditions : Conditions
        Object to store hydraulic systems power conditions with the following attributes:
            - power : numpy.ndarray
                Array to store the computed power draw values [W]
    conditions : Conditions
        Object containing mission conditions (not directly used in this function)
    
    Returns
    -------
    None
        This function modifies the hydraulics_conditions.power array in-place.
    
    Notes
    -----
    This function assigns the constant power draw value from the hydraulic systems component
    to the power array in the hydraulics_conditions object. The power draw is assumed
    to be constant throughout the mission segment.
    
    For more complex hydraulic systems models, this function could be extended to calculate
    power draw based on operating mode, altitude, or other mission parameters.
    
    See Also
    --------
    RCAIDE.Library.Methods.Powertrain.Systems.append_hydraulics_conditions
    """
    # 1. Define The Baseline (A320-200 parameters from MDPI Paper)
    MTOW_baseline = 75166.0 # kg
    P_res         = 3.52    # Reservoir pressure (bar)
    eta_pump      = 0.855   # 85.5% pump efficiency
    
    # Triple Hydraulics Systems (flow rates in L/min, System Pressures in bar)
    systems = {
        'Left':   {'n_pumps': 1, 'V_flow_base': 140.0, 'P_sys': 204.0},
        'Right':  {'n_pumps': 1, 'V_flow_base': 140.0, 'P_sys': 204.0},
        'Center': {'n_pumps': 1, 'V_flow_base': 23.0,  'P_sys': 196.0}
    }
    
    P_hydraulic = 0
    
    # 2. Extract current aircraft MTOW and compute scaling factor
    MTOW = vehicle.mass_properties.max_takeoff
    scaling_factor = MTOW / MTOW_baseline
    
    # 5. Compute power
    for name, sys in systems.items():
        
        # Scale the volumetric flow rate based on aircraft size
        V_flow = (sys['V_flow_base'] * scaling_factor) / 60000.0 # m^3/s
        
        # Pressure difference (System P - Reservoir P)
        delta_p = (sys['P_sys'] - P_res) * 100000.0 # Pa
        
        # Calculate mechanical pump power: P = (V_flow * Delta_P) / eta
        P_sys = sys['n_pumps'] * ((V_flow * delta_p) / eta_pump)
        
        P_hydraulic += P_sys
    
    P_act                            = P_hydraulic
          
    bus_conditions                   = state.conditions.energy.busses[bus.tag]
    hydraulics_conditions            = bus_conditions[hydraulics.tag]
    hydraulics_conditions.power[:,0] = P_act
    bus_conditions.power_draw       += hydraulics_conditions.power*bus.power_split_ratio /bus.efficiency    
    
    return 