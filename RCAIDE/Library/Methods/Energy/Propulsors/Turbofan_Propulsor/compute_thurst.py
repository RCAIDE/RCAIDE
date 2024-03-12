## @ingroup Methods-Energy-Propulsors-Turbofan_Propulsor
# RCAIDE/Methods/Energy/Propulsors/Turbofan_Propulsor/compute_thrust.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports  
from RCAIDE.Core      import Units 

# Python package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  compute_thrust
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Energy-Propulsors-Turbofan_Propulsor
def compute_thrust(turbofan,conditions,throttle = 1.0):
    """Computes thrust and other properties as below.

    Assumptions:
    Perfect gas

    Source:
    https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

    Inputs:
    conditions.freestream.
      isentropic_expansion_factor        [-] (gamma)
      specific_heat_at_constant_pressure [J/(kg K)]
      velocity                           [m/s]
      speed_of_sound                     [m/s]
      mach_number                        [-]
      pressure                           [Pa]
      gravity                            [m/s^2]
    conditions.throttle                  [-] (.1 is 10%)
    turbofan.inputs.
      fuel_to_air_ratio                  [-]
      total_temperature_reference        [K]
      total_pressure_reference           [Pa]
      core_nozzle.
        velocity                         [m/s]
        static_pressure                  [Pa]
        area_ratio                       [-]
      fan_nozzle.
        velocity                         [m/s]
        static_pressure                  [Pa]
        area_ratio                       [-]
      number_of_engines                  [-]
      bypass_ratio                       [-]
      flow_through_core                  [-] percentage of total flow (.1 is 10%)
      flow_through_fan                   [-] percentage of total flow (.1 is 10%)

    Outputs:
    turbofan.outputs.
      thrust                             [N]
      thrust_specific_fuel_consumption   [N/N-s]
      non_dimensional_thrust             [-]
      core_mass_flow_rate                [kg/s]
      fuel_flow_rate                     [kg/s]
      power                              [W]
      Specific Impulse                   [s]

    Properties Used:
    turbofan.
      reference_temperature              [K]
      reference_pressure                 [Pa]
      compressor_nondimensional_massflow [-]
      SFC_adjustment                     [-]
    """           
    #unpack the values

    #unpacking from conditions
    gamma                       = conditions.freestream.isentropic_expansion_factor 
    u0                          = conditions.freestream.velocity
    a0                          = conditions.freestream.speed_of_sound
    M0                          = conditions.freestream.mach_number
    p0                          = conditions.freestream.pressure  
    g                           = conditions.freestream.gravity        

    #unpacking from inputs
    f                           = turbofan.inputs.fuel_to_air_ratio
    total_temperature_reference = turbofan.inputs.total_temperature_reference
    total_pressure_reference    = turbofan.inputs.total_pressure_reference
    core_nozzle                 = turbofan.inputs.core_nozzle
    fan_nozzle                  = turbofan.inputs.fan_nozzle 
    fan_area_ratio              = turbofan.inputs.fan_nozzle.area_ratio
    core_area_ratio             = turbofan.inputs.core_nozzle.area_ratio                   
    bypass_ratio                = turbofan.inputs.bypass_ratio  
    flow_through_core           = turbofan.inputs.flow_through_core #scaled constant to turn on core thrust computation
    flow_through_fan            = turbofan.inputs.flow_through_fan #scaled constant to turn on fan thrust computation

    #unpacking from turbofan
    Tref                        = turbofan.reference_temperature
    Pref                        = turbofan.reference_pressure
    mdhc                        = turbofan.compressor_nondimensional_massflow
    SFC_adjustment              = turbofan.SFC_adjustment 

    #computing the non dimensional thrust
    core_thrust_nondimensional  = flow_through_core*(gamma*M0*M0*(core_nozzle.velocity/u0-1.) + core_area_ratio*(core_nozzle.static_pressure/p0-1.))
    fan_thrust_nondimensional   = flow_through_fan*(gamma*M0*M0*(fan_nozzle.velocity/u0-1.) + fan_area_ratio*(fan_nozzle.static_pressure/p0-1.))

    Thrust_nd                   = core_thrust_nondimensional + fan_thrust_nondimensional

    #Computing Specifc Thrust
    Fsp              = 1./(gamma*M0)*Thrust_nd

    #Computing the specific impulse
    Isp              = Fsp*a0*(1.+bypass_ratio)/(f*g)

    #Computing the TSFC
    TSFC             = f*g/(Fsp*a0*(1.+bypass_ratio))*(1.-SFC_adjustment) * Units.hour # 1/s is converted to 1/hr here
 
    #computing the core mass flow
    mdot_core        = mdhc*np.sqrt(Tref/total_temperature_reference)*(total_pressure_reference/Pref)

    #computing the dimensional thrust
    FD2              = Fsp*a0*(1.+bypass_ratio)*mdot_core*throttle

    #fuel flow rate
    a = np.array([0.])        
    fuel_flow_rate   = np.fmax(FD2*TSFC/g,a)*1./Units.hour

    #computing the power 
    power            = FD2*u0

    #pack outputs

    turbofan.outputs.thrust                            = FD2 
    turbofan.outputs.thrust_specific_fuel_consumption  = TSFC
    turbofan.outputs.non_dimensional_thrust            = Fsp 
    turbofan.outputs.core_mass_flow_rate               = mdot_core
    turbofan.outputs.fuel_flow_rate                    = fuel_flow_rate    
    turbofan.outputs.power                             = power  
    turbofan.outputs.specific_impulse                  = Isp
    
    return  