## @ingroup Methods-Energy-Propulsors-Converters-DC_Motor
# RCAIDE/Library/Methods/Energy/Propulsors/Converters/DC_Motor/dc_motor_performance.py
# (c) Copyright 2023 Aerospace Research Community LLC
# 
# Created:  Jun 2024, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------    
# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  dc_motor_performance
# ----------------------------------------------------------------------------------------------------------------------           
## @ingroup Methods-Energy-Propulsors-Converters-DC_Motor
def compute_Q_from_omega_and_V(motor):
    """Calculates the motor's torque

    Assumptions:

    Source:
    None

    Args:
    motor.
      gear_ratio           [-]
      speed_constant       [radian/s/V]
      resistance           [ohm]
      outputs.omega        [radian/s]
      gearbox_efficiency   [-]
      expected_current     [A]
      no_load_current      [A]
      inputs.volage        [V]

    Returns:
    motor.outputs.torque    [N-m] 
 
    """
    
    Res   = motor.resistance
    etaG  = motor.gearbox_efficiency
    exp_i = motor.expected_current
    io    = motor.no_load_current + exp_i*(1-etaG)
    G     = motor.gear_ratio
    Kv    = motor.speed_constant/G
    v     = motor.inputs.voltage
    omega = motor.inputs.omega
    
    # Torque
    Q = ((v-omega/Kv)/Res -io)/Kv
    
    motor.outputs.torque = Q
    motor.outputs.omega  = omega

    return


# ----------------------------------------------------------------------------------------------------------------------
#  compute_omega_and_Q_from_Cp_and_V
# ----------------------------------------------------------------------------------------------------------------------           
## @ingroup Methods-Energy-Propulsors-Converters-DC_Motor
def compute_omega_and_Q_from_Cp_and_V(motor,conditions):
    """Calculates the motor's rotation rate

    Assumptions:
    Cp (power coefficient) is constant

    Source:
    None

    Args:
    conditions.
      freestream.velocity                    [m/s]
      freestream.density                     [kg/m^3]
      propulsion.propeller_power_coefficient [-]
    motor.inputs.voltage                      [V]

    motor.
      resistance                             [ohms]
      gearbox_efficiency                     [-]
      expected_current                       [A]
      no_load_current                        [A]
      gear_ratio                             [-]
      speed_constant                         [radian/s/V]
      propeller_radius                       [m]
      
    Returns:
    motor.outputs.
      torque                                 [Nm]
      omega                                  [radian/s] 
    """           
    # Unpack 
    rho   = conditions.freestream.density[:,0,None]
    Res   = motor.resistance
    etaG  = motor.gearbox_efficiency
    exp_i = motor.expected_current
    io    = motor.no_load_current + exp_i*(1-etaG)
    G     = motor.gear_ratio
    Kv    = motor.speed_constant/G
    R     = motor.rotor_radius
    v     = motor.inputs.voltage
    Cp    = motor.inputs.rotor_CP
    

    # Omega
    # This is solved by setting the torque of the motor equal to the torque of the prop
    # It assumes that the Cp is constant
    omega1  =   ((np.pi**(3./2.))*((- 16.*Cp*io*rho*(Kv*Kv*Kv)*(R*R*R*R*R)*(Res*Res) +
                16.*Cp*rho*v*(Kv*Kv*Kv)*(R*R*R*R*R)*Res + (np.pi*np.pi*np.pi))**(0.5) - 
                np.pi**(3./2.)))/(8.*Cp*(Kv*Kv)*(R*R*R*R*R)*Res*rho)
    omega1[np.isnan(omega1)] = 0.0
    
    Q = ((v-omega1/Kv)/Res -io)/Kv
    # store to outputs 
    
    motor.outputs.torque = Q
    motor.outputs.omega = omega1

    return


# ----------------------------------------------------------------------------------------------------------------------
# compute_I_from_omega_and_V
# ----------------------------------------------------------------------------------------------------------------------           
## @ingroup Methods-Energy-Propulsors-Converters-DC_Motor
def compute_I_from_omega_and_V(motor):
    """Calculates the motor's current

    Assumptions:

    Source:
    None

    Args:
    motor.
      gear_ratio           [-]
      speed_constant       [radian/s/V]
      resistance           [ohm]
      outputs.omega        [radian/s]
      gearbox_efficiency   [-]
      expected_current     [A]
      no_load_current      [A]
    motor.inputs.voltage   [V]

    Returns:
    motor.outputs.current  [A]
    conditions.
      propulsion.etam      [-]  
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



# ----------------------------------------------------------------------------------------------------------------------
# compute_V_and_I_from_omega_and_Kv
# ----------------------------------------------------------------------------------------------------------------------           
## @ingroup Methods-Energy-Propulsors-Converters-DC_Motor
def compute_V_and_I_from_omega_and_Kv(motor):
    """Calculates the motor's voltage and current

    Assumptions:

    Source:
    None

    Args:
    motor.
      gear_ratio           [-]
      speed_constant       [radian/s/V]
      resistance           [ohm]
      outputs.omega        [radian/s]
      gearbox_efficiency   [-]
      expected_current     [A]
      no_load_current      [A]

    Returns:
    motor.outputs.current   [A]
    conditions.
      propulsion.volage    [V]
    conditions.
      propulsion.etam      [-] 
 
    """                      
           
    Res   = motor.resistance
    etaG  = motor.gearbox_efficiency
    exp_i = motor.expected_current
    io    = motor.no_load_current + exp_i*(1-etaG)
    G     = motor.gear_ratio
    kv    = motor.speed_constant/G
    Q     = motor.inputs.torque
    omega = motor.inputs.omega        
    
    v = (Q*kv+io)*Res + omega/kv
    i = (v-omega/kv)/Res
    
    motor.outputs.voltage    = v
    motor.outputs.current    = i
    motor.outputs.efficiency = (1-io/i)*(1-i*Res/v)
    
    return