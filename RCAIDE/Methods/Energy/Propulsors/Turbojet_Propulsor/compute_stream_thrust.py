## @ingroup Methods-Energy-Propulsors-Turbojet_Propulsor
# RCAIDE/Methods/Energy/Propulsors/Turbojet_Propulsor/compute_stream_thrust.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 

# Python package imports
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# compute_stream_thrust
# ----------------------------------------------------------------------------------------------------------------------
## @ingroup Methods-Energy-Propulsors-Turbojet_Propulsor  
def compute_stream_thrust(self,conditions):  
    """Computes thrust and other properties as below. 

    Assumptions: 

    Source: 
    Heiser, William H., Pratt, D. T., Daley, D. H., and Unmeel, B. M., 
    "Hypersonic Airbreathing Propulsors", 1994 
    Chapter 4 - pgs. 175-180

    Inputs: 
    conditions.freestream. 
       isentropic_expansion_factor        [-]  
       specific_heat_at_constant_pressure [J/(kg K)] 
       velocity                           [m/s] 
       speed_of_sound                     [m/s] 
       mach_number                        [-] 
       pressure                           [Pa] 
       gravity                            [m/s^2] 
    conditions.throttle                  [-] (.1 is 10%) 

    self.inputs. 
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
        number_of_engines                [-] 
        bypass_ratio                     [-] 
        flow_through_core                [-] percentage of total flow (.1 is 10%) 
        flow_through_fan                 [-] percentage of total flow (.1 is 10%)

    Outputs: 
    self.outputs. 
      thrust                             [N] 
      thrust_specific_fuel_consumption   [N/N-s] 
      non_dimensional_thrust             [-] 
      core_mass_flow_rate                [kg/s] 
      fuel_flow_rate                     [kg/s] 
      power                              [W] 

    Properties Used: 
    self. 
      reference_temperature              [K] 
      reference_pressure                 [Pa] 
      compressor_nondimensional_massflow [-] 
    """            

    #unpack the values 

    #unpacking from conditions 
    u0                   = conditions.freestream.velocity 
    a0                   = conditions.freestream.speed_of_sound 
    T0                   = conditions.freestream.temperature 
    g                    = conditions.freestream.gravity 
    throttle             = conditions.propulsion.throttle   
    R                    = conditions.freestream.gas_specific_constant 

    #unpacking from inputs 
    f                           = self.inputs.fuel_to_air_ratio 
    total_temperature_reference = self.inputs.total_temperature_reference 
    total_pressure_reference    = self.inputs.total_pressure_reference 
    core_nozzle                 = self.inputs.core_nozzle 
    core_exit_temperature       = core_nozzle.temperature 
    core_exit_velocity          = core_nozzle.velocity 
    core_area_ratio             = core_nozzle.area_ratio 
    no_eng                      = self.inputs.number_of_engines                       

    #unpacking from self 
    Tref                 = self.reference_temperature 
    Pref                 = self.reference_pressure 
    mdhc                 = self.compressor_nondimensional_massflow 

    # --------Stream thrust method ---------------------------         
    Sa0         = u0*(1+R*T0/u0**2) 
    Sa10        = core_exit_velocity*(1+R*core_exit_temperature/core_exit_velocity**2) 
    Fsp         = ((1+f)*Sa10 - Sa0 - R*T0/u0*(core_area_ratio-1))/a0 

    #Computing the specific impulse 
    Isp              = Fsp*a0/(f*g) 

    #Computing the TSFC 
    TSFC             = f*g/(Fsp*a0) 

    #computing the core mass flow 
    mdot_core        = mdhc*np.sqrt(Tref/total_temperature_reference)*(total_pressure_reference/Pref) 

    #computing the dimensional thrust 
    FD2              = Fsp*a0*mdot_core*no_eng*throttle 

    #fuel flow rate 
    a = np.array([0.])         
    fuel_flow_rate   = np.fmax(FD2*TSFC/g,a)  

    #computing the power  
    power            = FD2*u0 

    #pack outputs      
    self.outputs.thrust                            = FD2  
    self.outputs.thrust_specific_fuel_consumption  = TSFC 
    self.outputs.non_dimensional_thrust            = Fsp  
    self.outputs.core_mass_flow_rate               = mdot_core 
    self.outputs.fuel_flow_rate                    = fuel_flow_rate     
    self.outputs.power                             = power
    self.outputs.specific_impulse                  = Isp

    return 
