## @ingroup Methods-Energy-Propulsors-Converters-Motor
# RCAIDE/Methods/Energy/Propulsors/Converters/Motor/compute_Q_from_omega_and_V.py
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
def compute_Q_from_omega_and_V(self):
    """Calculates the motor's torque

    Assumptions:

    Source:
    N/A

    Inputs:

    Outputs:
    self.outputs.torque    [N-m] 

    Properties Used:
    self.
      gear_ratio           [-]
      speed_constant       [radian/s/V]
      resistance           [ohm]
      outputs.omega        [radian/s]
      gearbox_efficiency   [-]
      expected_current     [A]
      no_load_current      [A]
      inputs.volage        [V]
    """
    
    Res   = self.resistance
    etaG  = self.gearbox_efficiency
    exp_i = self.expected_current
    io    = self.no_load_current + exp_i*(1-etaG)
    G     = self.gear_ratio
    Kv    = self.speed_constant/G
    v     = self.inputs.voltage
    omega = self.inputs.omega
    
    # Torque
    Q = ((v-omega/Kv)/Res -io)/Kv
    
    self.outputs.torque = Q
    self.outputs.omega  = omega

    return

