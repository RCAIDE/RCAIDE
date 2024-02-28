## @ingroup Methods-Energy-Propulsors-Converters-Motor
# RCAIDE/Methods/Energy/Propulsors/Converters/Motor/compute_V_and_I_from_omega_and_Kv.py
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
def compute_V_and_I_from_omega_and_Kv(self):
    """Calculates the motor's voltage and current

    Assumptions:

    Source:
    N/A

    Inputs:

    Outputs:
    self.outputs.current   [A]
    conditions.
      propulsion.volage    [V]
    conditions.
      propulsion.etam      [-] 

    Properties Used:
    self.
      gear_ratio           [-]
      speed_constant       [radian/s/V]
      resistance           [ohm]
      outputs.omega        [radian/s]
      gearbox_efficiency   [-]
      expected_current     [A]
      no_load_current      [A]
    """                      
           
    Res   = self.resistance
    etaG  = self.gearbox_efficiency
    exp_i = self.expected_current
    io    = self.no_load_current + exp_i*(1-etaG)
    G     = self.gear_ratio
    kv    = self.speed_constant/G
    Q     = self.inputs.torque
    omega = self.inputs.omega        
    
    v = (Q*kv+io)*Res + omega/kv
    i = (v-omega/kv)/Res
    
    self.outputs.voltage    = v
    self.outputs.current    = i
    self.outputs.efficiency = (1-io/i)*(1-i*Res/v)
    
    return