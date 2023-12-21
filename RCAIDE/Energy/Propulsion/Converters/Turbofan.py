## @ingroup Energy-Propulsion-Converters
# RCAIDE/Energy/Propulsors/Converters/Fan.py
# 
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports  
from RCAIDE.Core                                         import Data, Units 
from RCAIDE.Energy.Energy_Component                      import Energy_Component 

import numpy as np 

# ----------------------------------------------------------------------
#  Fan Component
# ----------------------------------------------------------------------
## @ingroup Energy-Propulsion-Converters
class Turbofan(Energy_Component):
    """This is a  turbofan component.
    
    Assumptions:
    None

    Source:
    None
    """ 
    def __defaults__(self):    
        # setting the default values
        self.tag                                      = 'Turbofan' 
        self.engine_length                            = 0.0
        self.bypass_ratio                             = 0.0 
        self.design_isa_deviation                     = 0.0
        self.design_altitude                          = 0.0
        self.SFC_adjustment                           = 0.0 # Less than 1 is a reduction
        self.compressor_nondimensional_massflow       = 0.0
        self.reference_temperature                    = 288.15
        self.reference_pressure                       = 1.01325*10**5 
        self.design_thrust                            = 0.0
        self.mass_flow_rate_design                    = 0.0
        self.OpenVSP_flow_through                     = False
        
        #areas needed for drag; not in there yet
        self.areas                                    = Data()
        self.areas.wetted                             = 0.0
        self.areas.maximum                            = 0.0
        self.areas.exit                               = 0.0
        self.areas.inflow                             = 0.0
                               
        self.inputs                                   = Data()
        self.outputs                                  = Data()
        
        self.inputs.fuel_to_air_ratio                 = 0.0
        self.outputs.thrust                           = 0.0 
        self.outputs.thrust_specific_fuel_consumption = 0.0
        self.outputs.specific_impulse                 = 0.0
        self.outputs.non_dimensional_thrust           = 0.0
        self.outputs.core_mass_flow_rate              = 0.0
        self.outputs.fuel_flow_rate                   = 0.0
        self.outputs.fuel_mass                        = 0.0
        self.outputs.power                            = 0.0 
      
    def compute_thrust(self,conditions,throttle = 1.0):
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
          number_of_engines                  [-]
          bypass_ratio                       [-]
          flow_through_core                  [-] percentage of total flow (.1 is 10%)
          flow_through_fan                   [-] percentage of total flow (.1 is 10%)

        Outputs:
        self.outputs.
          thrust                             [N]
          thrust_specific_fuel_consumption   [N/N-s]
          non_dimensional_thrust             [-]
          core_mass_flow_rate                [kg/s]
          fuel_flow_rate                     [kg/s]
          power                              [W]
          Specific Impulse                   [s]

        Properties Used:
        self.
          reference_temperature              [K]
          reference_pressure                 [Pa]
          compressor_nondimensional_massflow [-]
          SFC_adjustment                     [-]
        """           
        #unpack the values

        #unpacking from conditions
        gamma                       = conditions.freestream.isentropic_expansion_factor
        Cp                          = conditions.freestream.specific_heat_at_constant_pressure
        u0                          = conditions.freestream.velocity
        a0                          = conditions.freestream.speed_of_sound
        M0                          = conditions.freestream.mach_number
        p0                          = conditions.freestream.pressure  
        g                           = conditions.freestream.gravity        

        #unpacking from inputs
        f                           = self.inputs.fuel_to_air_ratio
        total_temperature_reference = self.inputs.total_temperature_reference
        total_pressure_reference    = self.inputs.total_pressure_reference
        core_nozzle                 = self.inputs.core_nozzle
        fan_nozzle                  = self.inputs.fan_nozzle
        fan_exit_velocity           = self.inputs.fan_nozzle.velocity
        core_exit_velocity          = self.inputs.core_nozzle.velocity
        fan_area_ratio              = self.inputs.fan_nozzle.area_ratio
        core_area_ratio             = self.inputs.core_nozzle.area_ratio                   
        bypass_ratio                = self.inputs.bypass_ratio  
        flow_through_core           = self.inputs.flow_through_core #scaled constant to turn on core thrust computation
        flow_through_fan            = self.inputs.flow_through_fan #scaled constant to turn on fan thrust computation

        #unpacking from self
        Tref                        = self.reference_temperature
        Pref                        = self.reference_pressure
        mdhc                        = self.compressor_nondimensional_massflow
        SFC_adjustment              = self.SFC_adjustment 
 
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

        self.outputs.thrust                            = FD2 
        self.outputs.thrust_specific_fuel_consumption  = TSFC
        self.outputs.non_dimensional_thrust            = Fsp 
        self.outputs.core_mass_flow_rate               = mdot_core
        self.outputs.fuel_flow_rate                    = fuel_flow_rate    
        self.outputs.power                             = power  
        self.outputs.specific_impulse                  = Isp
        
        return 

    def compute_stream_thrust(self,conditions):  
        """Computes thrust and other properties as below. 

        Assumptions: 

        Source: 
        Heiser, William H., Pratt, D. T., Daley, D. H., and Unmeel, B. M., 
        "Hypersonic Airbreathing Propulsion", 1994 
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

    def size_core(self,conditions):
        """Sizes the core flow for the design condition.

        Assumptions:
        Perfect gas

        Source:
        https://web.stanford.edu/~cantwell/AA283_Course_Material/AA283_Course_Notes/

        Inputs:
        conditions.freestream.speed_of_sound [m/s] (conditions is also passed to self.compute(..))
        self.inputs.
          bypass_ratio                       [-]
          total_temperature_reference        [K]
          total_pressure_reference           [Pa]
          number_of_engines                  [-]

        Outputs:
        self.outputs.non_dimensional_thrust  [-]

        Properties Used:
        self.
          reference_temperature              [K]
          reference_pressure                 [Pa]
          total_design                       [N] - Design thrust
        """             
        #unpack inputs
        a0                   = conditions.freestream.speed_of_sound
        throttle             = 1.0

        #unpack from self
        bypass_ratio                = self.inputs.bypass_ratio
        Tref                        = self.reference_temperature
        Pref                        = self.reference_pressure 

        total_temperature_reference = self.inputs.total_temperature_reference  # low pressure turbine output for turbofan
        total_pressure_reference    = self.inputs.total_pressure_reference 

        #compute nondimensional thrust
        self.compute_thrust(conditions)

        #unpack results 
        Fsp                         = self.outputs.non_dimensional_thrust

        #compute dimensional mass flow rates
        mdot_core                   = self.design_thrust/(Fsp*a0*(1+bypass_ratio)*throttle)  
        mdhc                        = mdot_core/ (np.sqrt(Tref/total_temperature_reference)*(total_pressure_reference/Pref))

        #pack outputs
        self.mass_flow_rate_design               = mdot_core
        self.compressor_nondimensional_massflow  = mdhc

        return

    def size_stream_thrust(self,conditions): 
        """Sizes the core flow for the design condition. 

           Assumptions: 
           Perfect gas 

           Source: 
           Heiser, William H., Pratt, D. T., Daley, D. H., and Unmeel, B. M., 
           "Hypersonic Airbreathing Propulsion", 1994 
           Chapter 4 - pgs. 175-180
           
           Inputs: 
           conditions.freestream.speed_of_sound [m/s] (conditions is also passed to self.compute(..)) 
           self.inputs. 
              bypass_ratio                       [-] 
              total_temperature_reference        [K] 
              total_pressure_reference           [Pa] 
              number_of_engines                  [-] 

            Outputs: 
              self.outputs.non_dimensional_thrust  [-] 

            Properties Used: 
            self. 
               reference_temperature              [K] 
               reference_pressure                 [Pa] 
               total_design                       [N] - Design thrust 
               """              

        # Unpack Inputs
        
        # Unpack Conditions
        a0                      = conditions.freestream.speed_of_sound 
        throttle                = 1.0 
        
        # Unpack from self 
        Tref                        = self.reference_temperature 
        Pref                        = self.reference_pressure  
        
        # Unpack from Inputs
        total_temperature_reference = self.inputs.total_temperature_reference  # low pressure turbine output for turbofan 
        total_pressure_reference    = self.inputs.total_pressure_reference 
        no_eng                      = self.inputs.number_of_engines 
        
        #compute nondimensional thrust 
        self.compute_stream_thrust(conditions) 
        
        #unpack results  
        Fsp                         = self.outputs.non_dimensional_thrust 
        
        #compute dimensional mass flow rates 
        mdot_core                   = self.design_thrust/(Fsp*a0*no_eng*throttle)   
        mdhc                        = mdot_core/ (np.sqrt(Tref/total_temperature_reference)*(total_pressure_reference/Pref)) 
        
        #pack outputs 
        self.mass_flow_rate_design               = mdot_core 
        self.compressor_nondimensional_massflow  = mdhc 
        
        return        
        