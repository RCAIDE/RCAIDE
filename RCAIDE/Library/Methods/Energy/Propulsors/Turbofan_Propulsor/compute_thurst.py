## @ingroup Library-Methods-Energy-Propulsors-Turbofan_Propulsor
# RCAIDE/Library/Methods/Energy/Propulsors/Turbofan_Propulsor/compute_thrust.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports  
from RCAIDE.Framework.Core      import Units

# Python package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  compute_thrust
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Library-Methods-Energy-Propulsors-Turbofan_Propulsor
def compute_thrust(turbofan,conditions,throttle = 1.0):
    """Computes thrust and other properties of the turbofan listed below: 
    turbofan.  
      .outputs.thrust                           (numpy.ndarray): thrust                     [N] 
      .outputs.thrust_specific_fuel_consumption (numpy.ndarray): TSFC                       [N/N-s] 
      .outputs.non_dimensional_thrust           (numpy.ndarray): non-dim thurst             [unitless] 
      .outputs.core_mass_flow_rate              (numpy.ndarray): core nozzle mass flow rate [kg/s] 
      .outputs.fuel_flow_rate                   (numpy.ndarray): fuel flow rate             [kg/s] 
      .outputs.power                            (numpy.ndarray): power                      [W] 
      
    Assumptions:
        Perfect gas

    Source:
        Stanford AA 283 Course Notes: https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/


    Args: 
        conditions. 
           freestream.isentropic_expansion_factor                (float): isentropic expansion factor   [unitless]  
           freestream.specific_heat_at_constant_pressure         (float): speific heat                  [J/(kg K)] 
           freestream.velocity                           (numpy.ndarray): freestream velocity           [m/s] 
           freestream.speed_of_sound                     (numpy.ndarray): freestream speed_of_sound     [m/s] 
           freestream.mach_number                        (numpy.ndarray): freestream mach_number        [unitless] 
           freestream.pressure                           (numpy.ndarray): freestream pressure           [Pa] 
           freestream.gravity                            (numpy.ndarray): freestream gravity            [m/s^2] 
           propulsion.throttle                           (numpy.ndarray): throttle                      [unitless] 
        turbofan 
           .inputs.fuel_to_air_ratio                          (float): fuel_to_air_ratio                    [unitless] 
           .inputs.total_temperature_reference                (float): total_temperature_reference          [K] 
           .inputs.total_pressure_reference                   (float): total_pressure_reference             [Pa]    
           .core_nozzle.velocity                      (numpy.ndarray): turbofan core nozzle velocity        [m/s] 
           .core_nozzle.static_pressure               (numpy.ndarray): turbofan core nozzle static pressure [Pa] 
           .core_nozzle.area_ratio                            (float): turbofan core nozzle area ratio      [unitless] 
           .fan_nozzle.velocity                       (numpy.ndarray): turbofan fan nozzle velocity         [m/s] 
           .fan_nozzle.static_pressure                (numpy.ndarray): turbofan fan nozzle static pressure  [Pa] 
           .fan_nozzle.area_ratio                             (float): turbofan fan nozzle area ratio       [unitless]   
           .reference_temperature                             (float): reference_temperature                [K] 
           .reference_pressure                                (float): reference_pressure                   [Pa] 
           .compressor_nondimensional_massflow                (float): non-dim mass flow rate               [unitless]
      
    Returns:
        None
         
    """      
    # Unpack flight conditions 
    gamma                       = conditions.freestream.isentropic_expansion_factor 
    u0                          = conditions.freestream.velocity
    a0                          = conditions.freestream.speed_of_sound
    M0                          = conditions.freestream.mach_number
    p0                          = conditions.freestream.pressure  
    g                           = conditions.freestream.gravity        

    # Unpack turbofan operating conditions and properties 
    Tref                        = turbofan.reference_temperature
    Pref                        = turbofan.reference_pressure
    mdhc                        = turbofan.compressor_nondimensional_massflow
    SFC_adjustment              = turbofan.SFC_adjustment 
    f                           = turbofan.inputs.fuel_to_air_ratio
    total_temperature_reference = turbofan.inputs.total_temperature_reference
    total_pressure_reference    = turbofan.inputs.total_pressure_reference 
    flow_through_core           = turbofan.inputs.flow_through_core 
    flow_through_fan            = turbofan.inputs.flow_through_fan  
    V_fan_nozzle                = turbofan.inputs.fan_nozzle.velocity
    fan_area_ratio              = turbofan.inputs.fan_nozzle.area_ratio
    P_fan_nozzle                = turbofan.inputs.fan_nozzle.static_pressure
    P_core_nozzle               = turbofan.inputs.core_nozzle.static_pressure
    V_core_nozzle               = turbofan.inputs.core_nozzle.velocity
    core_area_ratio             = turbofan.inputs.core_nozzle.area_ratio                   
    bypass_ratio                = turbofan.inputs.bypass_ratio  

    # Compute  non dimensional thrust
    fan_thrust_nondim   = flow_through_fan*(gamma*M0*M0*(V_fan_nozzle/u0-1.) + fan_area_ratio*(P_fan_nozzle/p0-1.))
    core_thrust_nondim  = flow_through_core*(gamma*M0*M0*(V_core_nozzle/u0-1.) + core_area_ratio*(P_core_nozzle/p0-1.))

    thrust_nondim       = core_thrust_nondim + fan_thrust_nondim

    # Computing Specifc Thrust
    Fsp   = 1./(gamma*M0)*thrust_nondim

    # Compute specific impulse
    Isp   = Fsp*a0*(1.+bypass_ratio)/(f*g)

    # Compute TSFC
    TSFC  = f*g/(Fsp*a0*(1.+bypass_ratio))*(1.-SFC_adjustment) * Units.hour # 1/s is converted to 1/hr here
 
    # Compute core mass flow
    mdot_core  = mdhc*np.sqrt(Tref/total_temperature_reference)*(total_pressure_reference/Pref)

    # Compute dimensional thrust
    FD2  = Fsp*a0*(1.+bypass_ratio)*mdot_core*throttle

    # Compute power 
    power   = FD2*u0    

    # Compute fuel flow rate 
    fuel_flow_rate   = np.fmax(FD2*TSFC/g,np.array([0.]))*1./Units.hour

    # Pack turbofan outouts  
    turbofan.outputs.thrust                            = FD2 
    turbofan.outputs.thrust_specific_fuel_consumption  = TSFC
    turbofan.outputs.non_dimensional_thrust            = Fsp  
    turbofan.outputs.power                             = power  
    turbofan.outputs.specific_impulse                  = Isp
    turbofan.outputs.core_mass_flow_rate               = mdot_core
    turbofan.outputs.fuel_flow_rate                    = fuel_flow_rate   
    
    return  