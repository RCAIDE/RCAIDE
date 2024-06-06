# @ingroup Methods-Energy-Propulsors-Turboshaft_Propulsor
# RCAIDE/Library/Methods/Energy/Propulsors/Turboshaft_Propulsor/compute_power.py
# 
# 
# Created:  Jul 2023, M. Clarke
# Modified: Jun 2024, M. Guidotti & D.J. Lee

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# RCAIDE imports  
from RCAIDE.Framework.Core  import Units

# Python package imports
import numpy                as np

# ----------------------------------------------------------------------------------------------------------------------
#  compute_power
# ----------------------------------------------------------------------------------------------------------------------

def compute_power(turboshaft,conditions,throttle = 1.0):
    """Computes power and other properties as below.

    Assumptions:
    Perfect gas

    Source:
    Page 332 - 336
    https://soaneemrana.org/onewebmedia/ELEMENTS%20OF%20GAS%20TURBINE%20PROPULTION2.pdf 

    Inputs:
    conditions.freestream.
      isentropic_expansion_factor              [-] (gamma)
      specific_heat_at_constant_pressure       [J/(kg K)]
      velocity                                 [m/s]
      speed_of_sound                           [m/s]
      mach_number                              [-]
      pressure                                 [Pa]
      gravity                                  [m/s^2]
    conditions.throttle                        [-] (.1 is 10%)
    turboshaft.inputs.                         
      fuel_to_air_ratio                        [-]
      total_temperature_reference              [K]
      total_pressure_reference                 [Pa]
      core_nozzle.                             
        velocity                               [m/s]
        static_pressure                        [Pa]
        area_ratio                             [-]
      fan_nozzle.                              
        velocity                               [m/s]
        static_pressure                        [Pa]
        area_ratio                             [-]
      number_of_engines                        [-]
      bypass_ratio                             [-]
      flow_through_core                        [-] percentage of total flow (.1 is 10%)
      flow_through_fan                         [-] percentage of total flow (.1 is 10
    combustor.outputs.stagnation_temperature   [K]
    compressor.pressure_ratio                  [-]
                                               
    Outputs:                                   
    turboshaft.outputs.                        
      thrust                                   [N]
      non_dimensional_thrust                   [-]
      core_mass_flow_rate                      [kg/s]
      fuel_flow_rate                           [kg/s]
      power                                    [W]
      power_specific_fuel_consumption          [kg/(W*s)]
      Specific Impulse                         [s]
                                               
    Properties Used:                           
    turboshaft.                                
      reference_temperature                    [K]
      reference_pressure                       [Pa]
      compressor_nondimensional_massflow       [-]
      SFC_adjustment                           [-]
    """           
    #unpack the values

    #unpacking from conditions
    gamma                                      = conditions.freestream.isentropic_expansion_factor 
    u0                                         = conditions.freestream.velocity
    a0                                         = conditions.freestream.speed_of_sound
    M0                                         = conditions.freestream.mach_number
    p0                                         = conditions.freestream.pressure  
    g                                          = conditions.freestream.gravity 
    Cp                                         = conditions.freestream.specific_heat_at_constant_pressure    
                                               
    #unpacking from inputs                     
    f                                          = turboshaft.inputs.fuel_to_air_ratio
    total_temperature_reference                = turboshaft.inputs.total_temperature_reference
    total_pressure_reference                   = turboshaft.inputs.total_pressure_reference
    core_nozzle                                = turboshaft.inputs.core_nozzle
    fan_nozzle                                 = turboshaft.inputs.fan_nozzle  
    fan_area_ratio                             = turboshaft.inputs.fan_nozzle.area_ratio
    core_area_ratio                            = turboshaft.inputs.core_nozzle.area_ratio                   
    bypass_ratio                               = turboshaft.inputs.bypass_ratio  
    flow_through_core                          = turboshaft.inputs.flow_through_core #scaled constant to turn on core thrust computation
    flow_through_fan                           = turboshaft.inputs.flow_through_fan #scaled constant to turn on fan thrust computation

    #unpacking from turboshaft
    Tref                                       = turboshaft.reference_temperature
    Pref                                       = turboshaft.reference_pressure
    mdhc                                       = turboshaft.compressor_nondimensional_massflow
    SFC_adjustment                             = turboshaft.SFC_adjustment 
    Tt4                                        = turboshaft.combustor.outputs.stagnation_temperature
    pi_c                                       = turboshaft.compressor.pressure_ratio
                                               
    #computing the non dimensional power       
    tau_lambda                                 = Tt4/total_temperature_reference
    tau_r                                      = 1 + ((gamma - 1)/2)*M0**2
    tau_c                                      = pi_c**((gamma - 1)/gamma)
    Chi                                        = 1.02                                                       # Page 335
    C_shaft                                    = tau_lambda*(1 - Chi/(tau_r*tau_c)) - tau_r*(tau_c - 1)
    Power_nd                                   = Cp*total_temperature_reference*C_shaft
    
    
    
    
    
    flow_through_core*(gamma*M0*M0*(core_nozzle.velocity/u0-1.) + core_area_ratio*(core_nozzle.static_pressure/p0-1.))

    #Computing Specifc Power
    Fsp                                        = 1./(gamma*M0)*Thrust_nd
                                               
    #Computing the specific impulse            
    Isp                                        = Fsp*a0*(1.+bypass_ratio)/(f*g)
                                               
    #Computing the TSFC                        
    TSFC                                       = f*g/(Fsp*a0*(1.+bypass_ratio))*(1.-SFC_adjustment) * Units.hour # 1/s is converted to 1/hr here
                                               
    #computing the core mass flow              
    mdot_core                                  = mdhc*np.sqrt(Tref/total_temperature_reference)*(total_pressure_reference/Pref)
                                               
    #computing the dimensional thrust          
    FD2                                        = Fsp*a0*(1.+bypass_ratio)*mdot_core*throttle
                                               
    #fuel flow rate                            
    a = np.array([0.])                         
    fuel_flow_rate                             = np.fmax(FD2*TSFC/g,a)*1./Units.hour

    #computing the power 
    power                                      = FD2*u0

    #pack outputs

    turboshaft.outputs.thrust                            = FD2 
    turboshaft.outputs.thrust_specific_fuel_consumption  = TSFC
    turboshaft.outputs.non_dimensional_thrust            = Fsp 
    turboshaft.outputs.core_mass_flow_rate               = mdot_core
    turboshaft.outputs.fuel_flow_rate                    = fuel_flow_rate    
    turboshaft.outputs.power                             = power  
    turboshaft.outputs.specific_impulse                  = Isp

    return 