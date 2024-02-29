## @ingroup Methods-Energy-Propulsors-Turbojet_Propulsor
# RCAIDE/Methods/Energy/Propulsors/Turbojet_Propulsor/compute_thrust.py
# 
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
## @ingroup Methods-Energy-Propulsors-Turbojet_Propulsor
def compute_thrust(turbojet,conditions,throttle = 1.0):
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
    turbojet.inputs.
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
    turbojet.outputs.
      thrust                             [N]
      thrust_specific_fuel_consumption   [N/N-s]
      non_dimensional_thrust             [-]
      core_mass_flow_rate                [kg/s]
      fuel_flow_rate                     [kg/s]
      power                              [W]
      Specific Impulse                   [s]

    Properties Used:
    turbojet.
      reference_temperature              [K]
      reference_pressure                 [Pa]
      compressor_nondimensional_massflow [-]
      SFC_adjustment                     [-]
    """           
    #unpack the values

    #unpacking from conditions
    gamma                = conditions.freestream.isentropic_expansion_factor
    Cp                   = conditions.freestream.specific_heat_at_constant_pressure
    u0                   = conditions.freestream.velocity
    a0                   = conditions.freestream.speed_of_sound
    M0                   = conditions.freestream.mach_number
    p0                   = conditions.freestream.pressure  
    g                    = conditions.freestream.gravity        

    #unpacking from inputs
    f                           = turbojet.inputs.fuel_to_air_ratio
    total_temperature_reference = turbojet.inputs.total_temperature_reference
    total_pressure_reference    = turbojet.inputs.total_pressure_reference
    core_nozzle                 = turbojet.inputs.core_nozzle
    fan_nozzle                  = turbojet.inputs.fan_nozzle
    fan_exit_velocity           = turbojet.inputs.fan_nozzle.velocity
    core_exit_velocity          = turbojet.inputs.core_nozzle.velocity
    fan_area_ratio              = turbojet.inputs.fan_nozzle.area_ratio
    core_area_ratio             = turbojet.inputs.core_nozzle.area_ratio                   
    bypass_ratio                = turbojet.inputs.bypass_ratio  
    flow_through_core           = turbojet.inputs.flow_through_core #scaled constant to turn on core thrust computation
    flow_through_fan            = turbojet.inputs.flow_through_fan #scaled constant to turn on fan thrust computation

    #unpacking from turbojet
    Tref                 = turbojet.reference_temperature
    Pref                 = turbojet.reference_pressure
    mdhc                 = turbojet.compressor_nondimensional_massflow
    SFC_adjustment       = turbojet.SFC_adjustment 

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

    turbojet.outputs.thrust                            = FD2 
    turbojet.outputs.thrust_specific_fuel_consumption  = TSFC
    turbojet.outputs.non_dimensional_thrust            = Fsp 
    turbojet.outputs.core_mass_flow_rate               = mdot_core
    turbojet.outputs.fuel_flow_rate                    = fuel_flow_rate    
    turbojet.outputs.power                             = power  
    turbojet.outputs.specific_impulse                  = Isp

    return 