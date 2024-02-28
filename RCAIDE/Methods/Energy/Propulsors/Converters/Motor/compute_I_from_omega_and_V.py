## @ingroup Methods-Energy-Propulsors-Converters-Motor
# RCAIDE/Methods/Energy/Propulsors/Converters/Motor/compute_I_from_omega_and_V.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    
# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Motor  
# ----------------------------------------------------------------------------------------------------------------------           
## @ingroup Methods-Energy-Propulsors-Converters-Motor
def compute_I_from_omega_and_V(motor):
    """Calculates the motor's current

    Assumptions:

    Source:
    N/A

    Inputs:
    motor.inputs.voltage    [V]

    Outputs:
    motor.outputs.current   [A]
    conditions.
      propulsion.etam      [-] 

    Properties Used:
    motor.
      gear_ratio           [-]
      speed_constant       [radian/s/V]
      resistance           [ohm]
      outputs.omega        [radian/s]
      gearbox_efficiency   [-]
      expected_current     [A]
      no_load_current      [A]
    """                      
    
    # Unpack
    G     = motor.gear_ratio
    Kv    = motor.speed_constant
    Res   = motor.resistance
    v     = motor.inputs.voltage
    omeg  = motor.outputs.omega*G
    etaG  = motor.gearbox_efficiency
    exp_i = motor.expected_current
    io    = motor.no_load_current + exp_i*(1-etaG)
    
    i=(v-omeg/Kv)/Res
    
    # This line means the motor cannot recharge the battery
    i[i < 0.0] = 0.0

    # Pack
    motor.outputs.current    = i
    motor.outputs.efficiency = (1-io/i)*(1-i*Res/v)
    return