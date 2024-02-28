## @ingroup Methods-Energy-Propulsors-Converters-Motor
# RCAIDE/Methods/Energy/Propulsors/Converters/Motor/compute_omega_and_Q_from_Cp_and_V.py
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
def compute_omega_and_Q_from_Cp_and_V(self,conditions):
    """Calculates the motor's rotation rate

    Assumptions:
    Cp (power coefficient) is constant

    Source:
    N/A

    Inputs:
    conditions.
      freestream.velocity                    [m/s]
      freestream.density                     [kg/m^3]
      propulsion.propeller_power_coefficient [-]
    self.inputs.voltage                      [V]

    Outputs:
    self.outputs.
      torque                                 [Nm]
      omega                                  [radian/s]

    Properties Used:
    self.
      resistance                             [ohms]
      gearbox_efficiency                     [-]
      expected_current                       [A]
      no_load_current                        [A]
      gear_ratio                             [-]
      speed_constant                         [radian/s/V]
      propeller_radius                       [m]
    """           
    # Unpack 
    rho   = conditions.freestream.density[:,0,None]
    Res   = self.resistance
    etaG  = self.gearbox_efficiency
    exp_i = self.expected_current
    io    = self.no_load_current + exp_i*(1-etaG)
    G     = self.gear_ratio
    Kv    = self.speed_constant/G
    R     = self.rotor_radius
    v     = self.inputs.voltage
    Cp    = self.inputs.rotor_CP
    

    # Omega
    # This is solved by setting the torque of the motor equal to the torque of the prop
    # It assumes that the Cp is constant
    omega1  =   ((np.pi**(3./2.))*((- 16.*Cp*io*rho*(Kv*Kv*Kv)*(R*R*R*R*R)*(Res*Res) +
                16.*Cp*rho*v*(Kv*Kv*Kv)*(R*R*R*R*R)*Res + (np.pi*np.pi*np.pi))**(0.5) - 
                np.pi**(3./2.)))/(8.*Cp*(Kv*Kv)*(R*R*R*R*R)*Res*rho)
    omega1[np.isnan(omega1)] = 0.0
    
    Q = ((v-omega1/Kv)/Res -io)/Kv
    # store to outputs 
    
    self.outputs.torque = Q
    self.outputs.omega = omega1

    return