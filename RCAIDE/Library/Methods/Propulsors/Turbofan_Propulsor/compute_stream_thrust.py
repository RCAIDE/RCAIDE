# RCAIDE/Library/Methods/Propulsors/Turbofan_Propulsor/compute_stream_thrust.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# Python package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# compute_stream_thrust
# ----------------------------------------------------------------------------------------------------------------------  
def compute_stream_thrust(turbofan,conditions):  
    """Computes steam thrust and other properties of the turbofan listed below: 
    turbofan.  
      .outputs.thrust                           (numpy.ndarray): thrust                     [N] 
      .outputs.thrust_specific_fuel_consumption (numpy.ndarray): TSFC                       [N/N-s] 
      .outputs.non_dimensional_thrust           (numpy.ndarray): non-dim thurst             [unitless] 
      .outputs.core_mass_flow_rate              (numpy.ndarray): core nozzle mass flow rate [kg/s] 
      .outputs.fuel_flow_rate                   (numpy.ndarray): fuel flow rate             [kg/s] 
      .outputs.power                            (numpy.ndarray): power                      [W] 

    Assumptions: 
        None  
   
    Source: 
        Heiser, William H., Pratt, D. T., Daley, D. H., and Unmeel, B. M., 
        "Hypersonic Airbreathing Propulsors", 1994 
        Chapter 4 - pgs. 175-180
    
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
           .inputs.fuel_to_air_ratio                          (float): fuel_to_air_ratio                   [unitless] 
           .inputs.total_temperature_reference                (float): total_temperature_reference         [K] 
           .inputs.total_pressure_reference                   (float): total_pressure_reference            [Pa]   
           .core_nozzle.velocity                      (numpy.ndarray): turbofan core nozzle velocity        [m/s] 
           .core_nozzle.static_pressure               (numpy.ndarray): turbofan core nozzle static pressure [Pa] 
           .core_nozzle.area_ratio                            (float): turbofan core nozzle area ratio      [unitless]   
           .reference_temperature                             (float): reference_temperature                [K] 
           .reference_pressure                                (float): reference_pressure                   [Pa] 
           .compressor_nondimensional_massflow                (float): non-dim mass flow rate               [unitless]
      
    Returns:
        None 
    """            

    # Unpack turbofan properties 
    Tref             = turbofan.reference_temperature 
    Pref             = turbofan.reference_pressure 
    mdhc             = turbofan.compressor_nondimensional_massflow 
    f                = turbofan.inputs.fuel_to_air_ratio 
    Tt_ref           = turbofan.inputs.total_temperature_reference 
    Pt_ref           = turbofan.inputs.total_pressure_reference  
    Te_core          = turbofan.inputs.core_nozzle.temperature 
    Ve_core          = turbofan.inputs.core_nozzle.velocity 
    core_area_ratio  = turbofan.inputs.core_nozzle.area_ratio 
    no_eng           = turbofan.inputs.number_of_engines
    
    # Unpack flight conditions 
    u0        = conditions.freestream.velocity 
    a0        = conditions.freestream.speed_of_sound 
    T0        = conditions.freestream.temperature 
    g         = conditions.freestream.gravity 
    throttle  = conditions.propulsion.throttle   
    R         = conditions.freestream.gas_specific_constant 
  

    # Stream thrust method 
    Sa0       = u0*(1+R*T0/u0**2) 
    Sa10      = Ve_core*(1+R*Te_core/Ve_core**2) 
    Fsp       = ((1+f)*Sa10 - Sa0 - R*T0/u0*(core_area_ratio-1))/a0  

    #Compute the TSFC 
    TSFC      = f*g/(Fsp*a0)

    # Compute the specific impulse 
    Isp       = Fsp*a0/(f*g)     

    # Compute the core mass flow 
    mdot_core = mdhc*np.sqrt(Tref/Tt_ref)*(Pt_ref/Pref) 

    # Compute ensional thrust 
    FD2       = Fsp*a0*mdot_core*no_eng*throttle
    
    # Compute power 
    power     = FD2*u0
    
    # Compute fuel flow rate         
    fuel_flow_rate   = np.fmax(FD2*TSFC/g,np.array([0.]))  
 
    # Pack turbofan outptus      
    turbofan.outputs.thrust                            = FD2    
    turbofan.outputs.power                             = power
    turbofan.outputs.thrust_specific_fuel_consumption  = TSFC 
    turbofan.outputs.specific_impulse                  = Isp
    turbofan.outputs.non_dimensional_thrust            = Fsp  
    turbofan.outputs.core_mass_flow_rate               = mdot_core 
    turbofan.outputs.fuel_flow_rate                    = fuel_flow_rate   
    
    return  