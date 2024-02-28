## @ingroup Energy-Propulsors-Converters
# RCAIDE/Energy/Propulsors/Converters/Motor.py
# 
# 
# Created:  Jul 2023, M. Clarke 

# ----------------------------------------------------------------------------------------------------------------------
#  IMPORT
# ----------------------------------------------------------------------------------------------------------------------   
# RCAIDE imports  
from RCAIDE.Energy.Energy_Component import Energy_Component

# package imports 
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
#  Motor  
# ----------------------------------------------------------------------------------------------------------------------           
## @ingroup Energy-Propulsors-Converters 
class Motor(Energy_Component):
    """This is a motor component.
    
    Assumptions:
    None

    Source:
    None
    """      
    def __defaults__(self):
        """This sets the default values for the component to function.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        None
        """           
        self.tag                = 'motor' 
        self.resistance         = 0.0
        self.no_load_current    = 0.0
        self.speed_constant     = 0.0
        self.rotor_radius       = 0.0
        self.rotor_Cp           = 0.0
        self.efficiency         = 1.0
        self.gear_ratio         = 1.0
        self.gearbox_efficiency = 1.0
        self.expected_current   = 0.0
        self.power_split_ratio  = 0.0
        self.design_torque      = 0.0
        self.wing_mounted       = False
        self.interpolated_func  = None