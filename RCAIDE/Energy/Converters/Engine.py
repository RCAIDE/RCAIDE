## @ingroup Components-Energy-Converters
# RCAIDE/Energy/Converters/Engine.py
# (c) Copyright The Board of Trustees of RCAIDE
# 
# Created:  Jul 2023, M. Clarke

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ---------------------------------------------------------------------------------------------------------------------- 
 # RCAIDE imports 
import RCAIDE
from RCAIDE.Core                                         import Units 
from RCAIDE.Energy.Energy_Component                      import Energy_Component  

# package imports
import numpy as np 

# ---------------------------------------------------------------------------------------------------------------------- 
#  Engine Class
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Components-Energy-Converters
class Engine(Energy_Component):
    """This is an internal combustion engine component.
    
    Assumptions:
    None

    Source:
    None
    """           
    def __defaults__(self):
        self.tag                             = 'internal_combustion_engine' 
        self.sea_level_power                 = 0.0
        self.flat_rate_altitude              = 0.0
        self.rated_speed                     = 0.0
        self.inputs.speed                    = 0.0
        self.power_specific_fuel_consumption = 0.36 

    def power(self,conditions,throttle):
        """ The internal combustion engine output power and specific power consumption
        
        Source:
        N/A
        
        Assumtions:
        Available power based on Gagg and Ferrar model (ref: S. Gudmundsson, 2014 - eq. 7-16)
        
        Inputs:
            Engine:
                sea-level power
                flat rate altitude
                rated_speed (RPM)
                throttle setting
                inputs.speed (RPM)
            Freestream conditions:
                altitude
                delta_isa
        Outputs:
            Brake power (or Shaft power)
            Power (brake) specific fuel consumption
            Fuel flow
            Torque
        """

        # Unpack
        altitude                         = conditions.freestream.altitude
        delta_isa                        = conditions.freestream.delta_ISA 
        PSLS                             = self.sea_level_power
        h_flat                           = self.flat_rate_altitude
        speed                            = self.inputs.speed
        power_specific_fuel_consumption  = self.power_specific_fuel_consumption

        # shift in power lapse due to flat rate
        altitude_virtual = altitude - h_flat       
        altitude_virtual[altitude_virtual<0.] = 0. 
        
        atmo             = RCAIDE.Analyses.Atmospheric.US_Standard_1976()
        atmo_values      = atmo.compute_values(altitude_virtual,delta_isa) 
        rho              = atmo_values.density
        a                = atmo_values.speed_of_sound 

        # computing the sea-level ISA atmosphere conditions
        atmo_values = atmo.compute_values(0,0) 
        rho0        = atmo_values.density[0,0] 

        # calculating the density ratio:
        sigma = rho / rho0
 
        Pavailable                    = PSLS * (sigma - 0.117) / 0.883        
        Pavailable[h_flat > altitude] = PSLS

        # applying throttle setting
        output_power                  = Pavailable * throttle 
        output_power[output_power<0.] = 0. 
        SFC                           = power_specific_fuel_consumption * Units['lb/hp/hr']

        #fuel flow rate
        a               = np.zeros_like(altitude)
        fuel_flow_rate  = np.fmax(output_power*SFC,a)

        #torque
        torque = output_power/speed
        
        # store to outputs
        self.outputs.power                           = output_power
        self.outputs.power_specific_fuel_consumption = power_specific_fuel_consumption
        self.outputs.fuel_flow_rate                  = fuel_flow_rate
        self.outputs.torque                          = torque

        return self.outputs
    
    
    def calculate_throttle(self,conditions):
        """ The internal combustion engine output power and specific power consumption
        
        Source:
        N/A
        
        Assumtions:
        Available power based on Gagg and Ferrar model (ref: S. Gudmundsson, 2014 - eq. 7-16)
        
        Inputs:
            Engine:
                sea-level power
                flat rate altitude
                rated_speed (RPM)
                throttle setting
                inputs.power
            Freestream conditions:
                altitude
                delta_isa
        Outputs:
            Brake power (or Shaft power)
            Power (brake) specific fuel consumption
            Fuel flow
            Torque
            throttle setting
        """

        # Unpack
        altitude                         = conditions.freestream.altitude
        delta_isa                        = conditions.freestream.delta_ISA
        PSLS                             = self.sea_level_power
        h_flat                           = self.flat_rate_altitude
        power_specific_fuel_consumption  = self.power_specific_fuel_consumption
        output_power                     = self.inputs.power*1.0


        altitude_virtual = altitude - h_flat        
        altitude_virtual[altitude_virtual<0.] = 0.  
        
        atmo             = RCAIDE.Analyses.Atmospheric.US_Standard_1976()
        atmo_values      = atmo.compute_values(altitude_virtual,delta_isa) 
        rho              = atmo_values.density
        a                = atmo_values.speed_of_sound 

        # computing the sea-level ISA atmosphere conditions
        atmo_values = atmo.compute_values(0,0) 
        rho0        = atmo_values.density[0,0] 

        # calculating the density ratio 
        sigma = rho / rho0
 
        Pavailable                    = PSLS * (sigma - 0.117) / 0.883        
        Pavailable[h_flat > altitude] = PSLS


        # applying throttle setting
        throttle = output_power/Pavailable 
        output_power[output_power<0.] = 0. 
        SFC                           = power_specific_fuel_consumption * Units['lb/hp/hr']

        #fuel flow rate
        a               = np.zeros_like(altitude)
        fuel_flow_rate  = np.fmax(output_power*SFC,a)

        
        # store to outputs
        self.outputs.power_specific_fuel_consumption = power_specific_fuel_consumption
        self.outputs.fuel_flow_rate                  = fuel_flow_rate
        self.outputs.throttle                        = throttle

        return self.outputs    

