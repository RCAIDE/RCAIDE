## @ingroup Methods-Energy-Propulsors-Converters-Engine
# RCAIDE/Library/Methods/Energy/Propulsors/Converters/Engine/compute_power_from_throttle.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    
 # RCAIDE imports 
import RCAIDE
from RCAIDE.Framework.Core                                         import Units

# package imports
import numpy as np 

# ---------------------------------------------------------------------------------------------------------------------- 
# compute_power_from_throttle
# ----------------------------------------------------------------------------------------------------------------------   
## @ingroup Energy-Propulsors-Converters-Engine
def compute_power_from_throttle(engine,conditions,throttle):
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
            inputs.omega
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
    PSLS                             = engine.sea_level_power
    h_flat                           = engine.flat_rate_altitude
    omega                            = engine.inputs.speed
    power_specific_fuel_consumption  = engine.power_specific_fuel_consumption

    # shift in power lapse due to flat rate
    altitude_virtual = altitude - h_flat       
    altitude_virtual[altitude_virtual<0.] = 0. 
    
    atmo             = RCAIDE.Framework.Analyses.Atmospheric.US_Standard_1976()
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
    torque = output_power/omega
    
    # store to outputs
    engine.outputs.power                           = output_power
    engine.outputs.power_specific_fuel_consumption = power_specific_fuel_consumption
    engine.outputs.fuel_flow_rate                  = fuel_flow_rate
    engine.outputs.torque                          = torque

    return



def _compute_power_from_throttle(State, Settings, System):
	'''
	Framework version of compute_power_from_throttle.
	Wraps compute_power_from_throttle with State, Settings, System pack/unpack.
	Please see compute_power_from_throttle documentation for more details.
	'''

	#TODO: engine     = [Replace With State, Settings, or System Attribute]
	#TODO: conditions = [Replace With State, Settings, or System Attribute]
	#TODO: throttle   = [Replace With State, Settings, or System Attribute]

	results = compute_power_from_throttle('engine', 'conditions', 'throttle')
	#TODO: [Replace results with the output of the original function]

	State, Settings, System = results
	#TODO: [Replace packing with correct attributes]

	return State, Settings, System