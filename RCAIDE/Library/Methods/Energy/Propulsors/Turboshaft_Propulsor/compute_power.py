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
from RCAIDE.Framework.Core                 import Units
from RCAIDE.Library.Attributes.Propellants import Jet_A1 as Propellant

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
    turboshaft.conversion_efficiency           [-]
                                               
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
    
    LHV                                        = 1000*Propellant.lower_heating_value  # 1000 to match units from kJ/kg to J/kg

    #unpacking from conditions
    gamma                                      = conditions.freestream.isentropic_expansion_factor 
    #u0                                         = conditions.freestream.velocity
    a0                                         = conditions.freestream.speed_of_sound
    M0                                         = conditions.freestream.mach_number
    #p0                                         = conditions.freestream.pressure  
    #g                                          = conditions.freestream.gravity 
    Cp                                         = conditions.freestream.specific_heat_at_constant_pressure 
                                               
    #unpacking from inputs                     
    #f                                          = turboshaft.inputs.fuel_to_air_ratio
    total_temperature_reference                = turboshaft.inputs.total_temperature_reference
    total_pressure_reference                   = turboshaft.inputs.total_pressure_reference
    #core_nozzle                                = turboshaft.inputs.core_nozzle
    #fan_nozzle                                 = turboshaft.inputs.fan_nozzle  
    #fan_area_ratio                             = turboshaft.inputs.fan_nozzle.area_ratio
    #core_area_ratio                            = turboshaft.inputs.core_nozzle.area_ratio                   
    #bypass_ratio                               = turboshaft.inputs.bypass_ratio  
    #flow_through_core                          = turboshaft.inputs.flow_through_core #scaled constant to turn on core thrust computation
    #flow_through_fan                           = turboshaft.inputs.flow_through_fan #scaled constant to turn on fan thrust computation
    #eta_c                                      = turboshaft.conversion_efficiency

    #unpacking from turboshaft
    Tref                                       = turboshaft.reference_temperature
    Pref                                       = turboshaft.reference_pressure
    mdhc                                       = turboshaft.compressor_nondimensional_massflow
    #SFC_adjustment                             = turboshaft.SFC_adjustment 
    Tt4                                        = turboshaft.combustor.outputs.stagnation_temperature
    pi_c                                       = turboshaft.compressor.pressure_ratio
                                                     
    tau_lambda                                 = Tt4/total_temperature_reference
    tau_r                                      = 1 + ((gamma - 1)/2)*M0**2
    tau_c                                      = pi_c**((gamma - 1)/gamma)
    #tau_t                                      = (1/(tau_r*tau_c)) + ((gamma - 1)*M0**2)/(2*tau_lambda*eta_c**2)
    tau_t                                      = Chi/(tau_r*tau_c)
    Chi                                        = 1.02                                                       # Page 335
    C_shaft                                    = tau_lambda*(1 - Chi/(tau_r*tau_c)) - tau_r*(tau_c - 1)

    #Computing Specifc Thrust
    #Tsp                                        = a0*(((2/(gamma - 1))*(tau_lambda/(tau_r*tau_c))*(tau_r*tau_c*tau_t - 1))**(0.5) - M0)
    
    #Computing Specifc Power
    Psp                                        = Cp*total_temperature_reference*C_shaft
    
    #computing the core mass flow              
    mdot_core                                  = mdhc*np.sqrt(Tref/total_temperature_reference)*(total_pressure_reference/Pref)    
    
    #Computing Power 
    #Power                                      = Psp*mdot_core
    Power                                      = mdot_core*Cp*total_temperature_reference*(tau_lambda*(1 - tau_t) - tau_r*(tau_c - 1))
    
    #Computing the PSFC                        
    PSFC                                       = (tau_lambda/(C_shaft*LHV))
                                                                                                       
    #fuel flow rate                             
    fuel_flow_rate                             = Power*PSFC*1./Units.hour

    #pack outputs

    turboshaft.outputs.power_specific_fuel_consumption   = PSFC
    turboshaft.outputs.core_mass_flow_rate               = mdot_core
    turboshaft.outputs.fuel_flow_rate                    = fuel_flow_rate    
    turboshaft.outputs.power                             = Power
    turboshaft.outputs.non_dimensional_power             = Psp

    return 