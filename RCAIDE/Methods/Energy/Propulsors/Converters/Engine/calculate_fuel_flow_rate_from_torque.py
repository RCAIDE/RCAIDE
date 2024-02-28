## @ingroup Methods-Energy-Propulsors-Converters-Engine
# RCAIDE/Methods/Energy/Propulsors/Converters/Engine/calculate_fuel_flow_rate_from_torque.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    
 # RCAIDE imports 
import RCAIDE
from RCAIDE.Core                                         import Units  

# package imports
import numpy as np 

# ---------------------------------------------------------------------------------------------------------------------- 
# calculate_fuel_flow_rate_from_torque
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Energy-Propulsors-Converters-Engine
def calculate_fuel_flow_rate_from_torque(engine,conditions):
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
    PSLS                             = engine.sea_level_power
    h_flat                           = engine.flat_rate_altitude
    power_specific_fuel_consumption  = engine.power_specific_fuel_consumption
    omega                            = engine.outputs.omega
    torque                           = engine.outputs.torque

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

    output_power    = torque * omega
    a               = np.zeros_like(altitude)
    SFC             = power_specific_fuel_consumption * Units['lb/hp/hr']
    fuel_flow_rate  = np.fmax(output_power*SFC,a)
    throttle        = output_power/Pavailable
    output_power[output_power<0.] = 0.

    # store to outputs
    engine.outputs.power_specific_fuel_consumption = power_specific_fuel_consumption
    engine.outputs.fuel_flow_rate                  = fuel_flow_rate
    engine.outputs.throttle                        = throttle
    engine.outputs.power                           = output_power

    return

